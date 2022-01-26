from pydantic import BaseModel
from typing import Optional, List


class Installment(BaseModel):
    name: str
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
    install_unique_id: str
    student_unique_id: str
    patch: Optional[bool] = False


class Student(BaseModel):
    name: str
    school: str
    branch_id: int
    governorate_id: str
    institute_id: str
    state_unique_id: str
    first_phone: Optional[str] = None
    second_phone: Optional[str] = None
    code: int
    telegram_user: Optional[str] = None
    created_at: str
    note: Optional[str] = None
    total_amount: float
    poster: int
    remaining_amount: float
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
    authority: List[Authority]
    unique_id: str

    class Config:
        orm_mode = True
