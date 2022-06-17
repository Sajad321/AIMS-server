from fastapi import APIRouter
from tortoise.transactions import in_transaction
from schemas.general import AttendanceSchema, StudentAttendanceSchema
from models.models import Attendance, StudentAttendance, Students

attendance_router = APIRouter()


# attendance new adding 'POST' or edit
@attendance_router.post('/attendance')
async def add_attendance(schema: AttendanceSchema):
    if schema.patch is True:
        await Attendance.filter(unique_id=schema.unique_id).delete()
    stu_attendance = await Attendance.filter(unique_id=schema.unique_id).all()
    for unique in stu_attendance:
        if unique.unique_id == schema.unique_id:
            return {
                False
            }
    async with in_transaction() as conn:
        if schema.patch is True:
            new = Attendance(
                name=schema.name, unique_id=schema.unique_id, patch_state=1)
        else:
            new = Attendance(name=schema.name, unique_id=schema.unique_id)
        await new.save(using_db=conn)
    return {
        True
    }


# receive new students_attendance
@attendance_router.post('/student-attendance')
async def post_student_attendance(schema: StudentAttendanceSchema):
    if schema.patch is True:
        await StudentAttendance.filter(unique_id=schema.unique_id).delete()
    student = await Students.filter(unique_id=schema.student_unique_id).first()
    old_attendance = await Attendance.filter(unique_id=schema.attendance_unique_id).first()
    async with in_transaction() as conn:
        if schema.patch is True:

            new = StudentAttendance(time=schema.time, attendance_id=old_attendance.id,
                                    attended=schema.attended, student_id=student.id,
                                    unique_id=schema.unique_id, patch_state=1)
        else:
            new = StudentAttendance(time=schema.time, attendance_id=old_attendance.id,
                                    attended=schema.attended, student_id=student.id,
                                    unique_id=schema.unique_id,)
        await new.save(using_db=conn)
    return {
        True
    }


@attendance_router.get('/attendance')
async def get_attendance():
    return {
        "attendance": await Attendance.all()
    }


# to get all or patched student attendance
@attendance_router.get('/student-attendance')
async def get_student_attendance():
    query = await StudentAttendance.all().prefetch_related('student', 'attendance')
    return {
        "students_attendance": [n.__dict__ for n in query]
    }
