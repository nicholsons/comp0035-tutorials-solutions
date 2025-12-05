import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from playing_cards.playing_cards import Deck, Rank, Suit, create_cards


@pytest.fixture
def deck_cards():
    suit_values = [Suit(suit=s) for s in ['Clubs', 'Diamonds', 'Hearts', 'Spades']]
    rank_values = [Rank(rank=str(r)) for r in
                   [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']]
    deck_cards = Deck(suits=suit_values, ranks=rank_values)
    yield deck_cards


@pytest.fixture(scope='function')
def session_fixture():
    """" Populate an in-memory database

    Add tables for suits, ranks and cards

    """
    # Create the cards
    suits, ranks, cards = create_cards()

    # Create an in-memory database session and yield
    engine = create_engine(
        "sqlite:///:memory:",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all(suits)
        session.add_all(ranks)
        session.add_all(cards)
        session.commit()
        yield session
