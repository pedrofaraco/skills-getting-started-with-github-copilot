"""Tests for DELETE /activities/{activity_name}/participants/{email} endpoint"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering from activities"""

    def test_successful_unregister(self, client):
        """Test successful unregister from an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Unregistered {email} from {activity_name}" in data["message"]

        # Verify the participant was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity_name]["participants"]

    def test_unregister_nonexistent_activity(self, client):
        """Test unregister from activity that doesn't exist"""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "test@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Activity not found"

    def test_unregister_not_signed_up(self, client):
        """Test unregister when student is not signed up"""
        # Arrange
        activity_name = "Chess Club"
        email = "notsignedup@mergington.edu"  # Not signed up

        # Act
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Student not signed up"

    def test_unregister_from_multiple_activities(self, client):
        """Test unregistering from multiple activities"""
        # Arrange - First sign up for two activities
        email = "multitest@mergington.edu"
        client.post("/activities/Chess Club/signup?email=multitest@mergington.edu")
        client.post("/activities/Programming Class/signup?email=multitest@mergington.edu")

        # Act - Unregister from both
        response1 = client.delete("/activities/Chess Club/participants/multitest@mergington.edu")
        response2 = client.delete("/activities/Programming Class/participants/multitest@mergington.edu")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify removed from both
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data["Chess Club"]["participants"]
        assert email not in activities_data["Programming Class"]["participants"]

    def test_unregister_with_spaces_in_activity_name(self, client):
        """Test unregister from activity with spaces in name"""
        # Arrange
        activity_name = "Programming Class"
        email = "spacetest@mergington.edu"

        # First sign up
        client.post(f"/activities/{activity_name}/signup?email={email}")

        # Act - Unregister
        response = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert f"Unregistered {email} from {activity_name}" in data["message"]

        # Verify removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity_name]["participants"]