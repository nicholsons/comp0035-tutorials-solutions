""" Example service for the Games model """
from __future__ import annotations

from typing import List, Sequence

from sqlmodel import Session, select

from para_app.models import Games


class GamesService:
    """ Paralympic games CRUD services """

    def __init__(self, session: Session):
        self.session = session

    def create_games(self, games: Games) -> Games:
        """ Create one games """
        self.session.add(games)
        self.session.commit()
        self.session.refresh(games)
        return games

    def create_many_games(self, games: List[Games]) -> str:
        """ Create many games """
        self.session.add_all(games)
        self.session.commit()
        return f"Multiple Paralympics created."

    def read_games(self, game_id: int) -> Games:
        """ Read one game """
        games = self.session.get(Games, game_id).one()
        return games

    def read_all_games(self) -> Sequence[Games]:
        """ Read all games """
        statement = select(Games)
        result = self.session.exec(statement).all()
        return result

    def delete_games(self, game_id: int) -> str:
        """ Delete Paralympics games by id """
        self.session.delete(game_id)
        self.session.commit()
        return f"Games with id {game_id} deleted."

    def update_games(self, games: Games) -> Games:
        """ Update games """
        self.session.add(games)
        self.session.commit()
        self.session.refresh(games)
        return games

