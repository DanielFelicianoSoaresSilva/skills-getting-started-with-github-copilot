from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_unregister_and_signup_cycle():
    # Ensure participant exists initially
    resp = client.get('/activities')
    assert resp.status_code == 200
    participants = resp.json()['Basketball']['participants']
    assert 'alex@mergington.edu' in participants

    # Unregister the participant
    resp = client.post('/activities/Basketball/unregister?email=alex@mergington.edu')
    assert resp.status_code == 200
    assert 'Unregistered alex@mergington.edu' in resp.json().get('message', '')

    # Unregistering again should return 400
    resp = client.post('/activities/Basketball/unregister?email=alex@mergington.edu')
    assert resp.status_code == 400

    # Sign up again should succeed
    resp = client.post('/activities/Basketball/signup?email=alex@mergington.edu')
    assert resp.status_code == 200
    assert 'Signed up alex@mergington.edu' in resp.json().get('message', '')
