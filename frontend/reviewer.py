import streamlit as st
import requests

BASE = "http://localhost:8000"

st.title("LLM RedTeam Review Queue")
if st.button("Refresh"):
    res = requests.get(f"{BASE}/review/pending").json()
    pending = res.get("pending", [])
else:
    pending = requests.get(f"{BASE}/review/pending").json().get("pending", [])

for item in pending:
    st.markdown(f"**ID:** {item['id']}  **Score:** {item['score']}  **Label:** {item['label']}")
    st.write(item['prompt'])
    col1, col2 = st.columns(2)
    if col1.button(f"Approve {item['id']}"):
        requests.post(f"{BASE}/review/resolve", json={"id":item['id'], "action":"APPROVE"})
    if col2.button(f"Block {item['id']}"):
        requests.post(f"{BASE}/review/resolve", json={"id":item['id'], "action":"BLOCK"})
