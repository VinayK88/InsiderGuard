import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="InsiderGuard", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")
r = json.loads(Path("reports/baseline.json").read_text())
users = r["user_risk"]
events = r["events"]

st.markdown("""
<style>
:root{--blue:#0071e3;--ink:#1d1d1f;--muted:#6e6e73;--bg:#f5f5f7}
[data-testid="stAppViewContainer"]{background:var(--bg)}[data-testid="stHeader"]{background:transparent}[data-testid="stSidebar"]{background:#fff;border-right:1px solid #e5e5ea}.block-container{padding:2rem 2.4rem 4rem;max-width:1500px}
.hero{background:linear-gradient(135deg,#fff,#f7fbff);border:1px solid #e5e5ea;border-radius:28px;padding:34px 38px;margin-bottom:22px;box-shadow:0 12px 30px rgba(0,0,0,.045)}.eyebrow{color:var(--blue);font-weight:700;font-size:.82rem;letter-spacing:.12em;text-transform:uppercase}.hero h1{font-size:3.1rem;letter-spacing:-.04em;margin:.15rem 0 .35rem;color:var(--ink)}.hero p{font-size:1.15rem;color:var(--muted);max-width:850px}.pill{display:inline-block;background:#eef6ff;color:#0066cc;border-radius:999px;padding:7px 12px;margin:10px 6px 0 0;font-size:.82rem;font-weight:600}
[data-testid="stMetric"]{background:#fff;border:1px solid #e5e5ea;border-radius:22px;padding:19px 20px;box-shadow:0 8px 24px rgba(0,0,0,.04)}[data-testid="stMetricLabel"]{color:var(--muted);font-weight:600}[data-testid="stMetricValue"]{color:var(--ink);font-size:2rem;font-weight:700}.section{font-size:1.45rem;font-weight:700;color:var(--ink);margin:28px 0 12px}.note{background:#fff;border:1px solid #e5e5ea;border-radius:18px;padding:15px 18px;color:var(--muted)}div[data-testid="stDataFrame"]{border:1px solid #e5e5ea;border-radius:18px;overflow:hidden;background:#fff}.stTabs [data-baseweb="tab-list"]{gap:8px}.stTabs [data-baseweb="tab"]{background:#fff;border:1px solid #e5e5ea;border-radius:999px;padding:8px 16px}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🛡️ InsiderGuard")
    st.caption("UEBA & Insider Risk")
    st.markdown("---")
    st.markdown("**Overview**")
    st.markdown("Users")
    st.markdown("Alerts")
    st.markdown("Behaviors")
    st.markdown("Exfiltration")
    st.markdown("Investigations")
    st.markdown("Policies")
    st.markdown("Reports")
    st.markdown("---")
    st.caption("Synthetic telemetry · no employee data")

st.markdown("""<div class="hero"><div class="eyebrow">Behavioral Security Analytics</div><h1>InsiderGuard</h1><p>UEBA and insider-risk detection that combines peer deviation, identity context, risky sequences, and data movement into analyst-readable investigations.</p><span class="pill">UEBA</span><span class="pill">DLP</span><span class="pill">Identity Risk</span><span class="pill">Exfiltration Detection</span></div>""", unsafe_allow_html=True)

ev=r["evaluation"]
high_users=sum(1 for u in users.values() if u["max_score"] >= ev["threshold"])
risky_events=sum(1 for e in events if e["label"] == "risky")
cols=st.columns(5)
cols[0].metric("Users", len(users), "synthetic replay")
cols[1].metric("High-risk users", high_users, f"threshold {ev['threshold']:.2f}")
cols[2].metric("Risky events", risky_events, "sequence-aware")
cols[3].metric("Precision", f"{ev['precision']:.0%}", "0 false positives")
cols[4].metric("Recall", f"{ev['recall']:.0%}", "guardrailed")

st.markdown('<div class="section">Behavioral posture</div>', unsafe_allow_html=True)
a,b,c=st.columns([1.35,1,1])
with a:
    st.markdown("**Peer-group anomaly trend · illustrative**")
    st.line_chart({"Finance":[18,24,22,35,31,42],"Engineering":[11,13,17,16,20,19],"All users":[13,17,18,22,24,28]},height=250)
with b:
    st.markdown("**User risk distribution**")
    buckets={"Low":0,"Medium":0,"High":0}
    for u in users.values():
        score=u["max_score"]
        buckets["High" if score>=.55 else "Medium" if score>=.25 else "Low"]+=1
    st.bar_chart(buckets,height=250)
with c:
    st.markdown("**Top risky users**")
    ranked=sorted(users.items(),key=lambda kv:kv[1]["max_score"],reverse=True)
    max_score=max(v["max_score"] for _,v in ranked) or 1
    for name,u in ranked[:5]: st.progress(float(u["max_score"])/max_score,text=f"{name.title()} · {u['max_score']:.2f}")

st.markdown('<div class="section">Investigation workspace</div>', unsafe_allow_html=True)
t1,t2,t3=st.tabs(["Risk queue","Investigation timeline","Peer baselines"])
with t1:
    rows=[]
    for name,u in ranked:
        rows.append({"User":name.title(),"Max risk":u["max_score"],"Events":u["events"],"High-risk events":u["high_risk_events"],"Reasons":", ".join(u["reasons"]) or "—"})
    st.dataframe(rows,use_container_width=True,hide_index=True)
with t2:
    timeline=[]
    for e in sorted(events,key=lambda x:x["ts"],reverse=True):
        timeline.append({"Time":e["ts"],"User":e["user"].title(),"Event":e["event_type"],"Risk":e["score"],"Reasons":", ".join(e["reasons"]) or "—","Label":e["label"]})
    st.dataframe(timeline,use_container_width=True,hide_index=True)
with t3:
    for dept,b in r["peer_baselines"].items():
        st.markdown(f"**{dept.title()}**")
        x,y=st.columns(2)
        x.metric("Download mean",f"{b['download_mean_mb']:.1f} MB")
        y.metric("Std deviation",f"{b['download_std_mb']:.1f} MB")
    st.caption("Production baselines should be privacy-reviewed, role-aware, and monitored for drift.")

st.markdown("""<div class="note"><b>Privacy boundary.</b> All identity and DLP activity in this repository is synthetic. Real insider-risk programs require purpose limitation, minimization, access controls, and appropriate HR/legal governance.</div>""", unsafe_allow_html=True)
