from datetime import date

from activities.classes_wk5.classes_python import Athlete, AthleteWithMedals, Medal, ParalympicEvent, Runner


def main_activity5_1():
    # Activity 5.1 Create instance and use its methods
    event = ParalympicEvent(
        name="Men's individual BC1",
        sport="Boccia",
        classification="BC1",
    )
    event.describe()  # Should print the event description, "Athletes competing" will be empty
    event.register_athlete("Sungjoon Jung")  # should register the athlete
    event.describe()  # Should print the event again, "Athletes competing" should include Sungjoon Jung

    athlete = Athlete(first_name="Sungjoon Jung", last_name="Jung", team_code="CHN", disability_class="BC1")
    print(athlete)


def main_activity5_2():
    # Activity 5.2 Dataclass instance and print
    medal = Medal("gold", "Chaumet", date(2024, 1, 1))
    print(medal)


def main_activity5_3():
    # Activity 5.3 Inheritance example usage
    runner1 = Runner("Li", "Na", "CHN", "T12", "100m")
    runner1.introduce()  # Inherited method
    runner1.race_info()  # Subclass-specific method

    # Activity 5.3 Composition example
    # Create some medals
    medal1 = Medal("gold", "Paris 2024 design", date(2023, 7, 1))
    medal2 = Medal("silver", "Tokyo 2020 design", date(2019, 8, 25))

    # Create an athlete with medals
    # I added a new class called AthleteWithMedals in order to preserve the original Athlete function as an answer 5.1
    athlete2 = AthleteWithMedals(
        first_name="Wei",
        last_name="Wang",
        team_code="CHN",
        disability_class="T54",
        medals=[medal1, medal2]
    )
    print(athlete2)



if __name__ == "__main__":
    main_activity5_1()
    main_activity5_2()
    main_activity5_3()
