"""Tests for POST /activities/{activity_name}/signup endpoint"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up for activities"""

    def test_successful_signup(self, client):
        """Test successful signup for an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "test@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Signed up {email} for {activity_name}" in data["message"]

        # Verify the participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]

    def test_signup_nonexistent_activity(self, client):
        """Test signup for activity that doesn't exist"""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "test@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Activity not found"

    def test_duplicate_signup(self, client):
        """Test attempting to sign up for the same activity twice"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Student is already signed up"

    def test_signup_multiple_activities(self, client):
        """Test signing up for multiple different activities"""
        # Arrange
        email = "newstudent@mergington.edu"

        # Act - Sign up for two different activities
        response1 = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
        response2 = client.post("/activities/Programming Class/signup?email=newstudent@mergington.edu")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify in both activities
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data["Chess Club"]["participants"]
        assert email in activities_data["Programming Class"]["participants"]

    def test_signup_with_spaces_in_activity_name(self, client):
        """Test signup for activity with spaces in name"""
        # Arrange
        activity_name = "Programming Class"
        email = "spacetest@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert f"Signed up {email} for {activity_name}" in data["message"]

        # Verify the participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]