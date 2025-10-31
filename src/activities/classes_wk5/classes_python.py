from dataclasses import dataclass
from datetime import date
from typing import List


class ParalympicEvent:
    """ Represents a Paralympic event

     Attributes:
         name: A string representing the name of the event
         sport: An integer representing the sport that the event belongs to
         classification: An integer representing the event classification
         athletes: A list of strings representing the athletes that compete in the event

     Methods:
         describe() Prints a description of the event
         register_athlete() Adds an athlete to the list of athletes

     """

    def __init__(self, name, sport, classification):
        self.name = name
        self.sport = sport
        self.classification = classification
        self.athletes = []  # Empty list to hold athlete names

    def describe(self):
        """ Describes the event """
        print(f"{self.name} is a {self.sport} event for classification {self.classification}.")
        print("Athletes competing:", ", ".join(self.athletes))

    def register_athlete(self, athlete_name):
        """ Register the athlete with the event

        Args:
            athlete_name: A string representing the name of the athlete
        """
        self.athletes.append(athlete_name)


@dataclass
class Medal:
    """ Represents a Medal

    Attributes:
        type (str):  A string representing "gold", "silver", "bronze"
        design (str): A string description of the medal design
        date_designed (date): Date the medal was designed

    """
    type: str
    design: str
    date_designed: date


class Athlete:
    """ Represents an Athlete

        Attributes:
            first_name (str): The first name of the athlete.
            last_name (str): The last name of the athlete.
            team_code (str): The team code the athlete represents.
            disability_class (str): The disability classification of the athlete.

        Methods:
            __str__(): Returns a string representation of the athlete.
            introduce(): Prints an introduction of the athlete.
    """

    def __init__(self, first_name, last_name, team_code, disability_class):
        self.first_name = first_name
        self.last_name = last_name
        self.team_code = team_code
        self.disability_class = disability_class

    def __str__(self):
        """ Returns a string representation of the athlete.

            Returns:
                str: A string containing the athlete's full name, team code, and disability class.
        """
        return f"{self.first_name} {self.last_name} {self.team_code} {self.disability_class}"

    def introduce(self):
        """
                Prints an introduction of the athlete, including their name, team, and disability class.
                """
        print(f"{self.first_name} {self.last_name} represents {self.team_code} in class {self.disability_class}.")


class Runner(Athlete):
    """ Represents a Runner, inheriting from Athlete

        Attributes:
            distance (str): The distance the runner competes in (e.g., "100m", "400m").

        Methods:
            race_info(): Prints information about the runner's race.
    """

    def __init__(self, first_name, last_name, team_code, disability_class, distance):
        super().__init__(first_name, last_name, team_code, disability_class)
        self.distance = distance  # e.g., 100m, 400m

    def race_info(self):
        """ Prints information about the runner's race, including their name and distance."""
        print(f"{self.first_name} is running the {self.distance} race.")


# Type hints have been added to the constructor
class AthleteWithMedals:
    def __init__(self, first_name: str, last_name: str, team_code: str, disability_class: str, medals: List[Medal]):
        self.first_name = first_name
        self.last_name = last_name
        self.team_code = team_code
        self.disability_class = disability_class
        self.medals = medals  # Composition: Athlete has Medals

    def __str__(self):
        """ Returns a string representation of the athlete.

            Returns:
                str: A string containing the athlete's full name, team code, and disability class.
        """
        return f"{self.first_name} {self.last_name} {self.team_code} {self.disability_class} {self.medals}"

