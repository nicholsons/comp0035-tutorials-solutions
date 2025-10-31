""" Activity 5.4 Pydantic classes with validation"""
from datetime import date
from enum import Enum

from pydantic import BaseModel


# Not a pydantic class. Enumerator for the Medal. See https://docs.python.org/3/library/enum.html
class MedalType(Enum):
    BRONZE = 3
    SILVER = 2
    GOLD = 1


class Medal(BaseModel):
    """ Represents a Medal

    Attributes:
        type (MedalType):  A string representing "gold", "silver", "bronze"
        date_won (date):  Date the medal was won

    """
    type: MedalType
    date_won: date


class Athlete(BaseModel):
    """ Represents an Athlete

        Attributes:
            first_name (str): The first name of the athlete.
            last_name (str): The last name of the athlete.
            team_code (str): The team code the athlete represents.
            disability_class (str): The disability classification of the athlete.
            medals (list[Medal]): The medals the athlete has won.

        Methods:
            introduce(): Prints an introduction of the athlete.
    """
    first_name: str
    last_name: str
    team_code: str | None
    disability_class: str | None
    medals: list[Medal] = []

    def introduce(self) -> str:
        """
                Prints an introduction of the athlete, including their name, team, and disability class.
                """
        return f"{self.first_name} {self.last_name} represents {self.team_code} in class {self.disability_class}."


class ParalympicEvent(BaseModel):
    """ Represents a Paralympic event

     Attributes:
         name: A string representing the name of the event
         sport: An integer representing the sport that the event belongs to
         classification: An integer representing the event classification
         athletes: A list of strings representing the athletes that compete in the event

     Methods:
         register_athlete() Adds an athlete to the list of athletes

     """
    name: str
    sport: str
    classification: str
    athletes: list[Athlete]

    def register_athlete(self, athlete: Athlete):
        """ Register the athlete with the event

        Args:
            athlete (Athlete): The athlete to register
        """
        self.athletes.append(athlete)

