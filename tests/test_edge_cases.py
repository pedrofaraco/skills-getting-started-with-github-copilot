"""Tests for edge cases and error handling"""

import pytest
from urllib.parse import quote


class TestEdgeCases:
    """Test suite for edge cases and comprehensive error handling"""

    def test_signup_with_url_encoded_activity_name(self, client):
        """Test signup with URL-encoded activity name containing special characters"""
        # Arrange
        activity_name = "Programming Class"
        email = "urltest@mergington.edu"
        encoded_name = quote(activity_name)

        # Act
        response = client.post(f"/activities/{encoded_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert f"Signed up {email} for {activity_name}" in data["message"]

    def test_signup_with_empty_email(self, client):
        """Test signup with empty email parameter"""
        # Arrange
        activity_name = "Chess Club"
        email = ""

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert - Should succeed (no validation on email format in current implementation)
        assert response.status_code == 200
        data = response.json()
        assert f"Signed up {email} for {activity_name}" in data["message"]

    def test_signup_without_email_parameter(self, client):
        """Test signup without email query parameter"""
        # Arrange
        activity_name = "Chess Club"

        # Act
        response = client.post(f"/activities/{activity_name}/signup")

        # Assert - FastAPI should handle missing required parameter
        assert response.status_code == 422  # Unprocessable Entity for missing required param

    def test_get_activities_after_modifications(self, client):
        """Test that GET /activities reflects changes made by POST/DELETE"""
        # Arrange - Get initial state
        initial_response = client.get("/activities")
        initial_data = initial_response.json()
        initial_chess_count = len(initial_data["Chess Club"]["participants"])

        # Act - Add a participant
        new_email = "statecheck@mergington.edu"
        client.post("/activities/Chess Club/signup?email=statecheck@mergington.edu")

        # Assert - Check that the change is reflected
        updated_response = client.get("/activities")
        updated_data = updated_response.json()
        assert len(updated_data["Chess Club"]["participants"]) == initial_chess_count + 1
        assert new_email in updated_data["Chess Club"]["participants"]

    def test_state_persistence_across_requests(self, client):
        """Test that state persists correctly across multiple requests"""
        # Arrange
        email1 = "persist1@mergington.edu"
        email2 = "persist2@mergington.edu"

        # Act - Multiple operations
        client.post("/activities/Chess Club/signup?email=persist1@mergington.edu")
        client.post("/activities/Programming Class/signup?email=persist2@mergington.edu")
        client.delete("/activities/Chess Club/participants/persist1@mergington.edu")

        # Assert - Check final state
        final_response = client.get("/activities")
        final_data = final_response.json()

        assert email1 not in final_data["Chess Club"]["participants"]
        assert email2 in final_data["Programming Class"]["participants"]

    def test_case_sensitive_activity_names(self, client):
        """Test that activity names are case-sensitive"""
        # Arrange
        email = "casetest@mergington.edu"

        # Act - Try to signup with wrong case
        response = client.post("/activities/chess club/signup?email=casetest@mergington.edu")

        # Assert - Should fail because "chess club" != "Chess Club"
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Activity not found"

    def test_special_characters_in_email(self, client):
        """Test signup with special characters in email"""
        # Arrange
        activity_name = "Art Club"
        email = "test+special@mergington.edu"
        decoded_email = "test special@mergington.edu"  # FastAPI decodes + to space

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert f"Signed up {decoded_email} for {activity_name}" in data["message"]

        # Verify added with decoded email
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert decoded_email in activities_data[activity_name]["participants"]

    def test_unregister_same_email_twice(self, client):
        """Test attempting to unregister the same email twice"""
        # Arrange - Sign up first
        activity_name = "Debate Club"
        email = "doubleunreg@mergington.edu"
        client.post(f"/activities/{activity_name}/signup?email={email}")

        # Act - Unregister once (should succeed)
        response1 = client.delete(f"/activities/{activity_name}/participants/{email}")
        # Unregister again (should fail)
        response2 = client.delete(f"/activities/{activity_name}/participants/{email}")

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 404
        data2 = response2.json()
        assert data2["detail"] == "Student not signed up"