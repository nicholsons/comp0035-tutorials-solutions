""" Tests for activities in 9.2

Note: Some test cases are trivial or contrived, focus on learning how to structure and write the tests rather
than on what is being tested!
"""
import sys

import pytest
from sqlalchemy.exc import OperationalError
from sqlmodel import select

from playing_cards.playing_cards import CardModel, Deck, Rank, Suit, create_cards_db


def test_suit_returns_suitstring():
    """ Test that the suit returns the correct suit and datatype

        GIVEN a suit object
        WHEN the suit object's repr method is called
        THEN it should return a string with the value of Suit.suit
    """

    # Arrange: create a suit object and the expected result
    expected_result = "Hearts"
    suit = Suit(suit=expected_result)

    # Act: call its repr method
    result = suit.__repr__()

    # Assert
    assert result == expected_result
    assert type(result) == str


def test_deal_hand_return_amount():
    """ Test that the deal hand returns the correct amount of cards

    GIVEN a deck object
    WHEN the deal_hand method is called
    THEN it should return the amount of cards specified
    """
    # Arrange
    suit_values = [Suit(suit=s) for s in ['Clubs', 'Diamonds', 'Hearts', 'Spades']]
    rank_values = [Rank(rank=str(r)) for r in
                   [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']]
    deck_cards = Deck(suits=suit_values, ranks=rank_values)
    hand_size = 7

    # Act
    hand = deck_cards.deal_hand(hand_size)

    # Assert
    assert len(hand) == hand_size


def test_deal_hand_return_amount_fixture(deck_cards):
    """ Test that the deal hand returns the correct amount of cards

    This is for the activity that uses a fixture

    GIVEN a deck object
    WHEN the deal_hand method is called
    THEN it should return the amount of cards specified
    """
    # Arrange: deck_cards is now passed as a fixture to the test function
    hand_size = 7

    # Act
    hand = deck_cards.deal_hand(hand_size)

    # Assert
    assert len(hand) == hand_size


def test_deck_cards_count():
    """ Test that the deck cards count returns the correct number of cards

    This test is not strictly a unit test as it relies on the Suit and Rank classes

    GIVEN a deck of cards
    WHEN the deck is counted
    THEN the result should be 52 cards
    """

    # Arrange: create an instance of a deck
    suit_values = [Suit(suit=s) for s in ['Clubs', 'Diamonds', 'Hearts', 'Spades']]
    rank_values = [Rank(rank=str(r)) for r in
                   [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']]
    deck_cards = Deck(suits=suit_values, ranks=rank_values)

    # Act
    deck_length = len(deck_cards.deck)

    # Assert
    assert deck_length == 52


def test_deck_cards_count_fixture(deck_cards):
    """ Test that the deck cards count returns the correct number of cards

    This version uses a fixture

    This test is not strictly a unit test as it relies on the Suit and Rank classes

    GIVEN a deck of cards
    WHEN the deck is counted
    THEN the result should be 52 cards
    """

    # Arrange: deck_cards now comes from the fixture

    # Act
    deck_length = len(deck_cards.deck)

    # Assert
    assert deck_length == 52


def test_create_cards_db_raises_on_invalid_path():
    """Test that create_cards_db raises an exception if the DB path is invalid.

    GIVEN an invalid db path
    WHEN the create_cards_db is called
    THEN a sqlalchemy.exc OperationalError exception should be raised
    """

    # Arrange: An invalid path (directory, not a file)
    invalid_path = "/data"

    # Add test assertion here
    with pytest.raises(OperationalError):
        create_cards_db(invalid_path)


def test_select_returns_cards(session_fixture):
    """ Test that database returns results when the cards table is queried

    GIVEN an existing database in memory
    WHEN a query is made to the cards table
    THEN it should return a result set with 52 rows
    """
    statement = select(CardModel)
    result = session_fixture.exec(statement)
    cards = result.all()
    assert len(cards) == 52


if __name__ == '__main__':
    # pytest --cov=playing_cards --cov-report html:tests/playing_cards/htmlcov tests/playing_cards
    # Run tests under tests/playing_cards and generate HTML coverage for the playing_cards package
    sys.exit(pytest.main(
        ["-q", "--cov=src/playing_cards", "--cov-report html:tests/playing_cards/htmlcov",
         "tests/playing_cards"]))
