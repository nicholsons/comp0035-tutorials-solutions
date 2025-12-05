""" SQLModel classes for the students database. """
from sqlmodel import Field, Relationship, SQLModel


class Location(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    room: str

    courses: list["Course"] = Relationship(back_populates="location")


class Enrollment(SQLModel, table=True):
    student_id: int | None = Field(foreign_key="student.id", primary_key=True)
    course_id: int | None = Field(foreign_key="course.id", primary_key=True)
    teacher_id: int | None = Field(foreign_key="teacher.id", primary_key=True)


class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    student_name: str
    student_email: str

    courses: list["Course"] = Relationship(back_populates="students", link_model=Enrollment)
    teachers: list["Teacher"] = Relationship(back_populates="students", link_model=Enrollment)


class Teacher(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    teacher_name: str
    teacher_email: str

    courses: list["Course"] = Relationship(back_populates="teachers", link_model=Enrollment)
    students: list["Student"] = Relationship(back_populates="teachers", link_model=Enrollment)


class Course(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    course_name: str
    course_code: int
    course_schedule: str | None = None
    location_id: int | None = Field(foreign_key="location.id")

    students: list["Student"] = Relationship(back_populates="courses", link_model=Enrollment)
    teachers: list["Teacher"] = Relationship(back_populates="courses", link_model=Enrollment)
    location: "Location" = Relationship(back_populates="courses")
