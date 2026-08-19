import json
from pathlib import Path
import streamlit as st
st.set_page_config(page_title='InsiderGuard',layout='wide')
st.title('InsiderGuard — UEBA & Exfiltration Detection')
r=json.loads(Path('reports/baseline.json').read_text())
c=st.columns(4)
c[0].metric('Precision',r['evaluation']['precision']); c[1].metric('Recall',r['evaluation']['recall']); c[2].metric('FPR',r['evaluation']['fpr']); c[3].metric('Events',r['event_count'])
st.subheader('User risk'); st.json(r['user_risk'])
st.subheader('Investigation timeline'); st.dataframe(r['events'],use_container_width=True)
st.caption('Synthetic UEBA/DLP telemetry. No real employee data.')
