import random
from pathlib import Path
from typing import List

from sqlalchemy.exc import OperationalError
from sqlmodel import Field, SQLModel, Session, create_engine, Relationship

database_path = Path(__file__).parent.joinpath('test_deck.db')


class Suit(SQLModel, table=True):
    """ Suit for playing cards """
    suit_id: int | None = Field(default=None, primary_key=True)
    suit: str

    cards: List["CardModel"] = Relationship(back_populates="suit")

    def __repr__(self):
        """ Represents the suit as a string without the database id """
        return self.suit


class Rank(SQLModel, table=True):
    """ Rank for playing cards """
    rank_id: int | None = Field(default=None, primary_key=True)
    rank: str

    cards: List["CardModel"] = Relationship(back_populates="rank")

    def __repr__(self):
        """ Represents the rank as a string without the database id """
        return self.rank


class CardModel(SQLModel, table=True):
    """ Model for playing cards - database table version"""
    __tablename__ = "cards"

    rank_id: int | None = Field(primary_key=True, foreign_key="rank.rank_id")
    suit_id: int | None = Field(primary_key=True, foreign_key="suit.suit_id")

    rank: Rank | None = Relationship(back_populates="cards")
    suit: Suit | None = Relationship(back_populates="cards")


class Card:
    """ Card for playing cards """

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank


class Deck:
    """ Represents a deck of playing cards.

        This class provides methods to create, shuffle, draw, and deal cards from a deck.

        Attributes:
            suits (List[Suit]): List of Suit objects.
            ranks (List[Rank]): List of Rank objects.
            deck (List[Tuple[str, str]]): List of tuples representing the deck.

        Methods:
            create(): Creates a new deck.
            shuffle(): Shuffles the deck.
            draw(): Draws the deck.
            deal(): Deals the deck.

    """

    def __init__(self, suits: List[Suit], ranks: List[Rank]):
        self.suits = suits
        self.ranks = ranks
        self.deck = self.create_deck()

    def create_deck(self) -> List[tuple[str, str]]:
        return [(suit.suit, rank.rank) for suit in self.suits for rank in self.ranks]

    def shuffle(self) -> None:
        random.shuffle(self.deck)

    def draw_card(self) -> Card:
        card_vals = self.deck.pop()
        card = Card(*card_vals)
        return card

    def deal_hand(self, size) -> List[Card]:
        hand = []
        for i in range(size):
            hand.append(self.draw_card())
        # hand = None  # Deliberate bug!
        return hand


def create_cards_db(db_path):
    """ Creates a deck of cards database.

       Args:
           db_path (str or Path): The path to the SQLite database file.

       Returns:
           engine: SQLModel engine object.

        Raises:
            OperationalError: If an error occurs during database creation.
    """

    try:
        engine = create_engine(f"sqlite:///{db_path}", echo=True)
    except OperationalError as err:
        raise f"Cannot connect to DB {err}"
    else:
        SQLModel.metadata.create_all(engine)
        suits, ranks, cards = create_cards()

        with Session(engine) as session:
            session.add_all(suits)
            session.add_all(ranks)
            session.add_all(cards)
            session.commit()
            return engine


def create_cards():
    """ Create the objects that will be stored in the database """
    suits = [Suit(suit=s) for s in ['Clubs', 'Diamonds', 'Hearts', 'Spades']]
    ranks = [Rank(rank=str(r)) for r in [2, 3, 4, 5, 6, 7, 8, 9, 10, 'Jack', 'Queen', 'King', 'Ace']]
    cards = []
    for suit in suits:
        for rank in ranks:
            card = CardModel(suit=suit, rank=rank)
            cards.append(card)
    return [suits, ranks, cards]
