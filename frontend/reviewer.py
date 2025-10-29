import streamlit as st, requests
BASE = st.secrets.get('BACKEND_URL','http://localhost:8000')

st.title('LLM Review Queue')

if st.button('Refresh'):
    res = requests.get(f'{BASE}/review/pending').json()
else:
    res = requests.get(f'{BASE}/review/pending').json()

pending = res.get('pending', [])
for item in pending:
    st.markdown(f"**ID:** {item['id']}  **Score:** {item['score']}  **Label:** {item['label']}")
    st.write(item['prompt'])
    c1,c2 = st.columns(2)
    if c1.button(f"Approve_{item['id']}"):
        requests.post(f"{BASE}/review/resolve", json={'id': item['id'], 'action':'APPROVE'})
    if c2.button(f"Block_{item['id']}"):
        requests.post(f"{BASE}/review/resolve", json={'id': item['id'], 'action':'BLOCK'})

