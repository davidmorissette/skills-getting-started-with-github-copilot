def test_unregister_successfully_removes_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/participants", params={"email": email}
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities_response = client.get("/activities")
    activities_payload = activities_response.json()
    assert email not in activities_payload[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown%20Activity/participants", params={"email": "test@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_non_member_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/participants", params={"email": "notmember@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
