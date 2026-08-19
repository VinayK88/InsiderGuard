import argparse
import json
from pathlib import Path
from .models import Event
from .baselines import build_peer_baselines
from .detector import score_event
from .sequences import elevate_sequences,user_risk
from .evaluation import metrics

def load(path):
    out=[]
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        out.append(Event(**json.loads(line)))
    return out

def main():
    p=argparse.ArgumentParser(description='Replay synthetic insider-risk telemetry')
    p.add_argument('--input',default='sample_data/events.jsonl')
    p.add_argument('--output',default=None)
    a=p.parse_args()
    events=load(a.input)
    base=build_peer_baselines(events)
    scored=[score_event(e,base) for e in events]
    elevate_sequences(events,scored)
    payload={'event_count':len(events),'peer_baselines':base,'evaluation':metrics(scored),'user_risk':user_risk(scored),'events':scored}
    text=json.dumps(payload,indent=2)
    if a.output:
        Path(a.output).write_text(text+'\n', encoding='utf-8')
    print(text)

if __name__=='__main__':
    main()
