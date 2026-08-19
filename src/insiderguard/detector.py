from .baselines import download_z

BASE={"download":0.08,"external_share":0.22,"usb_write":0.28,"privilege_change":0.24,"mfa_reset":0.18,"cloud_upload":0.20,"login":0.03}

def score_event(e, baseline):
    score=BASE.get(e.event_type,0.05); reasons=[]
    if e.after_hours: score+=0.10; reasons.append('after_hours')
    if e.external: score+=0.14; reasons.append('external_destination')
    if e.new_country: score+=0.20; reasons.append('new_country')
    if e.privileged: score+=0.12; reasons.append('privileged_context')
    z=download_z(e,baseline)
    if z>=2: score+=min(0.35,0.08*z); reasons.append(f'peer_download_z:{z:.2f}')
    return {"event_id":e.event_id,"user":e.user,"event_type":e.event_type,"score":round(min(1.0,score),3),"reasons":reasons,"label":e.label,"ts":e.ts}
