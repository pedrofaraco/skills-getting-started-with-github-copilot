"""Tests for GET /activities endpoint"""

import pytest


class TestGetActivities:
    """Test suite for retrieving all activities"""

    def test_get_all_activities_success(self, client):
        """Test successful retrieval of all activities"""
        # Arrange - fixtures handle setup

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 9  # All 9 activities should be present

        # Check that all expected activities are present
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Soccer Club", "Art Club", "Drama Club", "Debate Club", "Science Club"
        ]
        for activity in expected_activities:
            assert activity in data

    def test_activity_structure(self, client):
        """Test that each activity has the correct structure"""
        # Arrange - fixtures handle setup

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Check structure of first activity (Chess Club)
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club

        assert isinstance(chess_club["participants"], list)
        assert isinstance(chess_club["max_participants"], int)

    def test_activity_data_accuracy(self, client):
        """Test that activity data is accurate"""
        # Arrange - fixtures handle setup

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Check specific activity data
        chess_club = data["Chess Club"]
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]

    def test_participant_counts(self, client):
        """Test that participant counts are correct"""
        # Arrange - fixtures handle setup

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Check participant counts for specific activities
        assert len(data["Chess Club"]["participants"]) == 2
        assert len(data["Programming Class"]["participants"]) == 2
        assert len(data["Basketball Team"]["participants"]) == 1