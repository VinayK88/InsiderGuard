from datetime import datetime

def elevate_sequences(events, scored, window_hours=8):
    by_user={}; score_by_id={r['event_id']:r for r in scored}
    for e in events: by_user.setdefault(e.user,[]).append(e)
    for user,rows in by_user.items():
        rows=sorted(rows,key=lambda e:e.ts)
        for i,e in enumerate(rows):
            if e.event_type!='privilege_change': continue
            start=datetime.fromisoformat(e.ts)
            tail=[]
            for x in rows[i+1:]:
                dt=datetime.fromisoformat(x.ts)
                if (dt-start).total_seconds() <= window_hours*3600: tail.append(x)
            types={x.event_type for x in tail}
            if 'download' in types and ({'external_share','usb_write','cloud_upload'} & types):
                ids=[e.event_id]+[x.event_id for x in tail]
                for eid in ids:
                    r=score_by_id[eid]; r['score']=round(min(1.0,r['score']+0.25),3); r['reasons']=r['reasons']+['risky_sequence']
    return scored

def user_risk(scored):
    users={}
    for r in scored:
        u=users.setdefault(r['user'],{"max_score":0.0,"events":0,"high_risk_events":0,"reasons":set()})
        u['max_score']=max(u['max_score'],r['score']); u['events']+=1
        if r['score']>=0.55: u['high_risk_events']+=1
        u['reasons'].update(r['reasons'])
    return {k:{**v,"reasons":sorted(v['reasons'])} for k,v in users.items()}
