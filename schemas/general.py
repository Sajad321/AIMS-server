from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class Installment(BaseModel):
    name: str
    date: Optional[str] = None
    unique_id: str
    patch: Optional[bool] = False


class State(BaseModel):
    name: str
    unique_id: str
    patch: Optional[bool] = False


class StudentInstallment(BaseModel):
    date: Optional[str] = None
    amount: Optional[int] = None
    invoice: Optional[int] = None
    unique_id: str
    received: Optional[int] = None
    install_unique_id: str
    student_unique_id: str
    patch: Optional[bool] = False


class StudentAttendanceSchema(BaseModel):
    time: Optional[str] = None
    unique_id: str
    attended: Optional[int] = None
    attendance_unique_id: str
    student_unique_id: str
    patch: Optional[bool] = False


class AttendanceSchema(BaseModel):
    unique_id: str
    institute_id: Optional[int]
    date: Optional[str] = None
    patch: Optional[bool] = False


class Student(BaseModel):
    name: str
    school: str
    branch_id: Optional[int]
    governorate_id: Optional[int]
    institute_id: Optional[int]
    state_unique_id: str
    first_phone: Optional[str] = None
    second_phone: Optional[str] = None
    code_1: Optional[str] = None
    code_2: Optional[str] = None
    qr: Optional[str] = None
    photo: Optional[str] = None
    dob: Optional[str] = None
    banned: Optional[int] = None
    telegram_user: Optional[str] = None
    created_at: Optional[str] = None
    note: Optional[str] = None
    total_amount: Optional[float]
    poster: Optional[int]
    remaining_amount: Optional[float]
    unique_id: str
    patch: Optional[bool] = False


class Del(BaseModel):
    unique_id_students: Optional[List[str]] = []
    unique_id_students_install: Optional[List[str]] = []
    unique_id_states: Optional[List[str]] = []
    unique_id_installment: Optional[List[str]] = []
    unique_id_users: Optional[List[str]] = []
    patch: Optional[bool] = False


class GetStudents(BaseModel):
    deleted: Optional[bool] = False


class Authority(BaseModel):
    state_unique_id: str
    unique_id: str

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    password: str
    super: Optional[int]
    authority: Optional[List[Authority]]
    unique_id: str
    name: Optional[str] = None

    class Config:
        orm_mode = True
