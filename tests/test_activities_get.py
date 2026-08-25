def test_get_activities_returns_activity_dictionary(client):
    # Arrange
    expected_activity_name = "Chess Club"

    # Act
    response = client.get("/activities")
    response_data = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(response_data, dict)
    assert expected_activity_name in response_data
    assert "participants" in response_data[expected_activity_name]
