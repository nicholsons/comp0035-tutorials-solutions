""" Tests for paralympic app in src/para_app

The SQLModel documentation for testing focuses on FastAPI apps which you do not have:
https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#pytest-fixtures

The following tutorial covers testing using only SQLModel:
 https://pytest-with-eric.com/database-testing/pytest-sql-database-testing/

Tests included:

    - Games instance with an invalid year
    - Games instance with a valid year
    - Calculate duration where the start_date and end_date are both present
    - Calculate duration where the start_date and end_date are not present
    - Calculate the mf ratio where the participants_m and participants_f are present
    - Calculate the mf ratio where the participants_m and participants_f are not present

"""
import pytest
from sqlalchemy.exc import IntegrityError

from para_app.models import Games


def test_calculate_duration():
    """
        Given a Games instance is created a valid start_date and end_date
        When the method 'calculate_duration' is called,
        Then it should return an integer in days of the event duration
    """
    # Arrange
    games = Games(event_type="summer", year=2020, start_date="12-12-2020", end_date="24-12-2020")
    # Act
    duration = games.calculate_duration()
    # Assert
    assert duration == 12


def test_calculate_duration_missing_date():
    """
        Given a Games instance with a valid missing start_date and valid end_date
        When the method 'calculate_duration' is called,
        Then it should raise a ValueError
    """
    games = Games(event_type="summer", year=2020, end_date="24-12-2020")
    with pytest.raises(ValueError):
        games.calculate_duration()


def test_create_games_with_valid_year():
    """
        Given a valid year
        When a Games instance is created,
        Then a Games instance is successfully created and the year value is present in the repr

        This test only tests the Games class so does not require any of the fixtures
    """
    games = Games(event_type="summer", year=2020)
    assert games.year == 2020
    assert '2020' in repr(games)  # included just to show the repr() method


def test_create_games_with_invalid_year():
    """
        Given an invalid year
        When a Games instance is created,
        Then a ValueError is raised

        This test only tests the Games class so does not require the fixtures
        SQLModel inherits from Pydantic but bypasses validation in the __init__
        One solution to call the .model_validate method instead
    """
    with pytest.raises(ValueError) as exc_info:
        Games.model_validate({"event_type": "summer", "year": 1959})
    assert "must be between 1960 and 9999" in str(exc_info.value)


def test_create_games_with_invalid_year_db(session_fixture):
    """
        Given a Games instance with an invalid year and a database fixture
        When the instance is committed,
        Then it should raise a sqlalchemy.exc.IntegrityError
    """
    invalid_game = Games(event_type="summer", year=1959)
    session_fixture.add(invalid_game)
    with pytest.raises(IntegrityError):
        session_fixture.commit()



# Calculate the mf ratio where the participants_m and participants_f are present
def test_calculate_ratio_values_present():
    """
    Given a Games instance with values for participants_m and participants_f
    When the method 'calculate_fm_ratio' is called,
    Then it should return a float representing the ratio of participants_m and participants_f
    """
    num_m = 120
    num_f = 12
    test_games = Games(event_type="summer", year=2020, participants_m=num_m, participants_f=num_f)
    expected_ratio = num_f/num_m
    assert test_games.calculate_fm_ratio() == expected_ratio


# Calculate the mf ratio where the participants_m and participants_f are not present
def test_calculate_ratio_values_missing():
    """
    Given a Games instance with missing values for participants_m and participants_f
    When the method 'calculate_fm_ratio' is called,
    Then it should raise a ValueError
    """
    test_games = Games(event_type="summer", year=2020, participants_f=12)
    with pytest.raises(ValueError):
        test_games.calculate_fm_ratio()
