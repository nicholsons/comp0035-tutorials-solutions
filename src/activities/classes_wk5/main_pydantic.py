from datetime import date

from pydantic import ValidationError

from activities.classes_wk5.classes_pydantic import Athlete, Medal, MedalType

if __name__ == "__main__":

    # Yuyan Jiang from team CHN People's Republic of China won 7 gold medals
    athlete = Athlete(first_name="Yuyan", last_name="Jiang", team_code="CHN", disability_class=None)
    # Create 7 golds medals
    medals = [Medal(type=MedalType.GOLD, date_won=date(2024, 7, i + 1)) for i in range(7)]
    # Add the medals to the athlete
    athlete.medals = medals
    # try each of the following to see the different output
    print(athlete)
    print(athlete.model_dump)
    print(athlete.model_dump_json())

    try:
        bp = Athlete(first_name="Bianka", medals=1)
    except ValidationError as e:
        for error in e.errors():
            print(error)
