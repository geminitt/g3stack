#!/usr/bin/env python3
"""Read-only native skill parsing in a temporary HOME; no turns/model calls.

Requires an installed Codex CLI with the inspected skills/list RPC schema.
Keeps its bounded diagnostic directory for evidence. Does not activate global
skills or change the user's actual config, model, authentication or history.
"""
from pathlib import Path
import json,os,selectors,shutil,signal,subprocess,tempfile,time
stage=Path(__file__).resolve().parent.parent
binary=shutil.which('codex')
if not binary:
 raise SystemExit('Codex CLI unavailable; native discovery remains unverified')
base=Path(tempfile.mkdtemp(prefix='g3-native-discovery-'))
home=base/'home';home.mkdir();(home/'.agents/skills').mkdir(parents=True);(home/'.codex').mkdir()
work=base/'project';work.mkdir()
expected={p.name for p in (stage/'codex/skills').iterdir()}
for name in expected:(home/'.agents/skills'/name).symlink_to(stage/'codex/skills'/name)
(home/'.agents/skills/task-router').symlink_to(stage/'.agents/skills/task-router')
env=dict(os.environ,HOME=str(home),CODEX_HOME=str(home/'.codex'),XDG_CONFIG_HOME=str(home/'.config'),XDG_CACHE_HOME=str(home/'.cache'),XDG_STATE_HOME=str(home/'.local/state'))
# No turns, threads, authentication, or model requests. Two read-only RPC calls.
log=(base/'stderr.log').open('w')
p=subprocess.Popen([binary,'app-server','--stdio'],cwd=work,env=env,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=log,start_new_session=True)
selector=selectors.DefaultSelector();selector.register(p.stdout,selectors.EVENT_READ)
messages=[];deadline=time.monotonic()+25

def send(item):p.stdin.write((json.dumps(item)+'\n').encode());p.stdin.flush()
def receive(request):
 while time.monotonic()<deadline:
  if not selector.select(.3):continue
  line=p.stdout.readline()
  if not line:raise RuntimeError('server closed output')
  item=json.loads(line);messages.append(item)
  if item.get('id')==request:return item
 raise TimeoutError('read-only native discovery deadline exceeded')
try:
 send({'id':1,'method':'initialize','params':{'clientInfo':{'name':'g3stack-packaging-check','version':'1'}}})
 initialized=receive(1)
 if 'error' in initialized:raise RuntimeError(str(initialized['error']))
 send({'method':'initialized','params':{}})
 send({'id':2,'method':'skills/list','params':{'cwds':[str(work)],'forceReload':True}})
 result=receive(2)
 if 'error' in result:raise RuntimeError(str(result['error']))
 (base/'responses.json').write_text(json.dumps(messages,indent=2)+'\n')
 data=result['result']['data'];skills=[s for entry in data for s in entry['skills']];errors=[e for entry in data for e in entry.get('errors',[])]
 actual={s['name'] for s in skills}
 receipt={'kind':'read-only native skills/list; no turn or model invocation','codex_version':subprocess.run([binary,'--version'],env=env,capture_output=True,text=True,timeout=5,check=True).stdout.strip(),'temporary_home':str(home),'workspace':str(work),'expected_skills':len(expected),'discovered_skills':sorted(expected & actual),'missing':sorted(expected-actual),'errors':errors,'main':next((s for s in skills if s['name']=='g3stack'),None),'evidence_directory':str(base)}
 (base/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({'expected':len(expected),'discovered':len(expected & actual),'missing':receipt['missing'],'errors':errors,'evidence_directory':str(base)}))
 assert not receipt['missing'] and not errors
finally:
 if p.poll() is None:os.killpg(p.pid,signal.SIGTERM)
 try:p.wait(timeout=3)
 except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=3)
 log.close()
