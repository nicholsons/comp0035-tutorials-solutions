""" Test the query_service.py module

To test the queries requires a database with data in.

The QueryService class required the engine_fixture

The db_with_data fixture adds data at the start of each test function and removes it at the end (function scope)

"""
from para_app.query_service import QueryService


def test_read_hosts(engine_fixture, db_with_data):
    """
    Given an instance of the query service
    When the .read_hosts() method is called
    Then at least 10 results should be returned AND 'Rome' should be in string format results
    """
    qs = QueryService(engine_fixture)
    result = qs.read_hosts()
    assert len(result) > 10
    assert "Rome" in str(result)


def test_read_host(engine_fixture, db_with_data):
    """
        Given an instance of the query service
        When the .read_host(1) method is called
        Then a Host object should be returned and its id should be 1
        """
    qs = QueryService(engine_fixture)
    host = qs.read_host(1)
    assert host.id == 1


def test_create_host(engine_fixture, db_with_data):
    """
    Given a place_name: str, and country_name: str that is in the database
    When the create_host() method is called
    Then a Host object should be returned and its place_name should match the place_name
    """
    qs = QueryService(engine_fixture)
    host = qs.create_host(place_name="Cape Town", country_name="South Africa")
    assert host.place_name == "Cape Town"

