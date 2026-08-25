import src.app as app_module


def test_signup_registers_student_successfully(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new-student@mergington.edu"
    participants_before = len(app_module.activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    participants_after = len(app_module.activities[activity_name]["participants"])
    assert participants_after == participants_before + 1
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_returns_400_for_duplicate_registration(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_returns_400_when_activity_is_full(client):
    # Arrange
    activity_name = "Test Full Activity"
    app_module.activities[activity_name] = {
        "description": "Temporary activity for full-capacity testing",
        "schedule": "Fridays, 4:00 PM - 5:00 PM",
        "max_participants": 1,
        "participants": ["existing@mergington.edu"],
    }
    email = "new@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Activity is full"}


def test_signup_returns_422_when_email_query_is_missing(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422
