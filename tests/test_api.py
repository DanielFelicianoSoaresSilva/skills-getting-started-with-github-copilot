from fastapi.testclient import TestClient
from src.app import app
import uuid

client = TestClient(app)


def unique_email():
    return f"test-{uuid.uuid4().hex}@example.com"


def test_get_activities():
    resp = client.get('/activities')
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert 'Basketball' in data


def test_signup_and_duplicate_and_cleanup():
    email = unique_email()

    # Successful signup
    resp = client.post(f"/activities/Basketball/signup?email={email}")
    assert resp.status_code == 200
    assert 'Signed up' in resp.json().get('message', '')

    # Duplicate signup should fail
    resp2 = client.post(f"/activities/Basketball/signup?email={email}")
    assert resp2.status_code == 400

    # Cleanup: unregister the test user
    resp3 = client.post(f"/activities/Basketball/unregister?email={email}")
    assert resp3.status_code == 200


def test_unregister_errors():
    email = unique_email()

    # Unregister for non-existent activity
    resp = client.post(f"/activities/NoSuchActivity/unregister?email={email}")
    assert resp.status_code == 404

    # Unregister a user who is not signed up should return 400
    resp2 = client.post(f"/activities/Basketball/unregister?email={email}")
    assert resp2.status_code == 400
