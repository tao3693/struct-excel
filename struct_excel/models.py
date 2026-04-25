from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class SessionMode(Enum):
    ONLINE = "online"
    OFFLINE = "offline"


@dataclass
class Student:
    student_id: int
    full_name: str
    email: str
    gender: Gender
    it_background: bool
    experience_min_years: int
    experience_max_years: int
    sector: str
    supervisor_id: int


@dataclass
class Course:
    course_id: int
    course_name: str
    duration: float


@dataclass
class Session:
    session_id: int
    course_id: int
    start_datetime: datetime
    end_datetime: datetime
    mode: SessionMode


@dataclass
class Supervisor:
    supervisor_id: int
    full_name: str
    email: str


@dataclass
class Enrollment:
    enrollment_id: int
    student_id: int
    session_id: int
    reg_date: datetime
    completed: bool
    payment_status: str
    exception: str
