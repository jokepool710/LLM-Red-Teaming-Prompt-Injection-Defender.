
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    r = client.get('/')
    assert r.status_code == 200
    assert 'running' in r.json().get('message','').lower()

def test_analyze_allow():
    payload = {'prompt': 'Hello, how are you?'}
    r = client.post('/ai/analyze', json=payload)
    assert r.status_code == 200
    data = r.json()
    assert 'action' in data
    assert data['action'] in ('ALLOW','QUEUE','BLOCK')

def test_analyze_block():
    payload = {'prompt': 'rm -rf /; sudo rm -rf /'}
    r = client.post('/ai/analyze', json=payload)
    assert r.status_code == 200
    data = r.json()
    assert 'action' in data

