from statistics import mean, pstdev

def build_peer_baselines(events):
    groups={}
    for e in events:
        groups.setdefault(e.department,[]).append(e.bytes_mb if e.event_type=='download' else 0.0)
    out={}
    for dept,vals in groups.items():
        mu=mean(vals) if vals else 0.0; sd=pstdev(vals) if len(vals)>1 else 1.0
        out[dept]={"download_mean_mb":round(mu,3),"download_std_mb":round(max(sd,1.0),3)}
    return out

def download_z(event, baseline):
    if event.event_type!='download': return 0.0
    b=baseline[event.department]
    return max(0.0,(event.bytes_mb-b['download_mean_mb'])/b['download_std_mb'])
