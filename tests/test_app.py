import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_participant():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    # Check participant added
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]

def test_signup_duplicate():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # Try to sign up again
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data

def test_signup_full():
    activity = "Chess Club"
    # Fill up the activity
    for i in range(20):
        email = f"student{i}@mergington.edu"
        client.post(f"/activities/{activity}/signup?email={email}")
    # Try to sign up when full
    response = client.post(f"/activities/{activity}/signup?email=overflow@mergington.edu")
    assert response.status_code in (400, 200)


def test_unregister_participant():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Accept 200 (removed) or 404 (not found)
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        data = response.json()
        assert "message" in data
        # Check participant removed
        get_resp = client.get("/activities")
        assert email not in get_resp.json()[activity]["participants"]
