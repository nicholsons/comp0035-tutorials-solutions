""" Queries from the week 8 activities """
from importlib import resources

import pandas as pd
from sqlmodel import Session, desc, select

from activities import data
from activities.database2_wk8.database import engine
from activities.database2_wk8.models import *

data_path = resources.files(data).joinpath("student_data.csv")


def add_teacher_data():
    """ Adds teacher data to the database."""
    cols = ["teacher_name", "teacher_email"]
    df = pd.read_csv(data_path, usecols=cols)

    # 2. Convert DataFrame rows to SQLModel instances and append to teachers list
    teachers = []
    for _, row in df.iterrows():
        record = Teacher(**row.to_dict())
        teachers.append(record)

    # 3. Insert all into database
    with Session(engine) as session:
        session.add_all(teachers)
        session.commit()


def add_all_data():
    """Adds data from CSV to each table using pandas DataFrame to filter the data. """
    df = pd.read_csv(data_path)

    # Find the unique location rows then create Location objects from these
    locations = df["course_location"].unique()
    loc_objects = []
    for loc in locations:
        location = Location(room=loc)
        loc_objects.append(location)

    # Find the unique student rows then create Student objects from these
    rows = df.drop_duplicates(subset=['student_name'])
    stu_objects = []
    for _, row in rows.iterrows():
        student = Student(student_name=row["student_name"], student_email=row["student_email"])
        stu_objects.append(student)

    # Find the unique teacher rows then create Teacher objects from these
    # You may have already added teacher data, in which case exclude this section
    rows = df.drop_duplicates(subset=['teacher_name'])
    teacher_objects = []
    for _, row in rows.iterrows():
        teacher = Teacher(teacher_name=row.teacher_name, teacher_email=row.teacher_email)
        teacher_objects.append(teacher)

    # Find the unique coutse rows then create Course objects from these
    rows = df.drop_duplicates(subset=['course_name'])
    course_objects = []
    for _, row in rows.iterrows():
        course = Course(course_name=row.course_name, course_code=row.course_code, course_schedule=row.course_schedule)
        course_objects.append(course)

    with Session(engine) as session:
        # Add the objects to the individual tables. Note there are no primary or foreign key values at this stage.
        # Once the objects are added to the database, the primary key value will be created
        session.add_all(loc_objects)
        session.add_all(stu_objects)
        session.add_all(teacher_objects)
        session.add_all(course_objects)
        session.commit()

        # Create and add the enrollment objects and add the location FK to the courses
        for _, row in df.iterrows():
            # Find the ids of the rows
            location = session.exec(select(Location).where(Location.room == row["course_location"])).first()
            course = session.exec(select(Course).where(Course.course_code == row["course_code"])).first()
            s_id = session.exec(select(Student.id).where(Student.student_email == row["student_email"])).first()
            t_id = session.exec(select(Teacher.id).where(Teacher.teacher_email == row["teacher_email"])).first()
            # Update the course with the location using the relationship attribute
            course.location = location
            # Create the new enrollment for the row
            enrollment = Enrollment(student_id=s_id, course_id=course.id, teacher_id=t_id)
            session.add_all([course, enrollment])
            session.commit()


def select_students():
    with Session(engine) as session:
        for student in session.exec(select(Student)):
            print(student)


def select_student():
    with Session(engine) as session:
        for student in session.exec(select(Student)):
            print(student)


def select_queries():
    """ Activity 8.5 """
    with Session(engine) as session:
        # select teacher where teacher_name == ""
        statement = select(Teacher).where(Teacher.teacher_name == "Mark Taylor")
        result = session.exec(statement)
        print("Teacher record: ", result.first())

        # select the names only for all the students
        statement = select(Student.student_name)
        result = session.exec(statement)
        students = result.all()
        print("\nAll students")
        for student in students:
            print(student)

        # Select all Student name and email that are enrolled on the Physics course, ordered by student name descending
        statement = select(Student.student_name, Student.student_email).join(Enrollment).join(Course).where(
            Course.course_name == "Physics").order_by(desc(Student.student_name))
        result = session.exec(statement)
        physics_students = result.all()
        print("\nAll students enrolled in Physics ordered by student name in descending order:")
        for student in physics_students:
            print(f"{student.student_name}, {student.student_email}")

        # Select all courses that student with id 1 is enrolled in
        statement = select(Course.course_code, Course.course_name).join(Enrollment).join(Student).where(
            Student.id == 1)
        result = session.exec(statement)
        courses = result.all()
        print("\nAll courses student with id 1 is enrolled in: ")
        for course in courses:
            print(course.course_code, course.course_name)


def update_queries():
    """ Activity 8.7 """

    # Update the course code for the Mathematics course to MATH102
    with Session(engine) as session:
        statement = select(Course).where(Course.course_name == "Mathematics")
        result = session.exec(statement)
        maths = result.first()
        print("\nMathematics record before: ", maths)
        maths.course_code = "MATH102"
        session.add(maths)
        session.commit()
        statement = select(Course).where(Course.course_name == "Mathematics")
        result = session.exec(statement)
        mathsnow = result.first()
        print("\nMathematics record after: ", mathsnow)

        # Update all teacher email addresses with the new domain @newschool.com. For this you also need Python string .replace()
        # e.g.  `.replace("@school.com", "@newschool.com")`
        statement = select(Teacher)
        result = session.exec(statement)
        teachers = result.all()
        print("\nAll teachers before update: ")
        for teacher in teachers: print(teacher.teacher_email)
        updated_teachers = []
        for teacher in teachers:
            teacher.teacher_email = teacher.teacher_email.replace("@school.com", "@newschool.com")
            updated_teachers.append(teacher)
        session.add_all(updated_teachers)
        session.commit()
        statement = select(Teacher)
        result = session.exec(statement)
        teachers = result.all()
        print("\nAll teachers after update: ")
        for teacher in teachers: print(teacher.teacher_email)


def delete_queries():
    """ Activity 8.6
    1. Delete the Teacher with name "John Smith"
    2. Delete the Enrollment for Student with student_id 1 from Course with Course_id 1
    """
    with Session(engine) as session:
        # Delete the Teacher with name "John Smith"
        teacher = session.exec(select(Teacher).where(Teacher.teacher_name == "John Smith")).first()
        if teacher:
            session.delete(teacher)
            session.commit()

        # Delete the Enrollment for Student with student_id 1 from Course with Course_id 1
        enrollment = session.exec(
            select(Enrollment).where(
                Enrollment.student_id == 1,
                Enrollment.course_id == 1
            )
        ).first()
        if enrollment:
            session.delete(enrollment)
            session.commit()
