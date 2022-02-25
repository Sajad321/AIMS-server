from fastapi import APIRouter
from tortoise.transactions import in_transaction
from schemas.general import Installment, State, StudentInstallment, Student, Del, GetStudents, User
from models.models import Installments, States, StudentInstallments, Students, Users, UserAuth, Branches, Governorates, \
    Institutes, Posters

general_router = APIRouter()


# GET `/users`
#
# - Get users from database.
# - Request Arguments: None
# - Returns: list of students.
#
# Example Response `{
#   "users": [
#     {
#       "id": 1,
#       "username": "krvhrv",
#       "authority": [
#         {
#           "authority_id": 1,
#           "state": "الكويت",
#           "state_id": 1
#         }
#       ]
#     }
#   ],
#   "total_users": 1,
#   "success": true
# }'
@general_router.get('/users')
async def get_users():
    users = await Users.all()
    result_list = []
    for user in users:
        result_json = {"id": user.id, "username": user.username, "unique_id": user.unique_id,"name": user.name,
                       "delete_state": user.delete_state, "password": user.password, "patch_state": user.patch_state}
        authority = []
        auth = await UserAuth.filter(user_id=user.id).prefetch_related('state').all()
        for au in auth:
            auth_json = {"authority_id": au.id, "state": au.state.name, "state_id": au.state.id,
                         "state_unique_id": au.state.unique_id,
                         "auth_unique_id": au.unique_id, "delete_state": au.delete_state}
            authority.append(auth_json)
        result_json['authority'] = authority
        result_list.append(result_json)
    return {
        "users": result_list,
        "total_users": await Users.all().count(),
        "success": True
    }


# POST `/users`
# - Add user in database.
# - Request Arguments: None
# - Returns: None.
# Example Request Payload `{
#     "username": "1",
#     "password": "22",
#     "authority": [
#         {
#             "state_id": 1,
#             "state": "نرس"
#         }
#     ],
# }`
# Example Response `{
#     "success": true
# }`
@general_router.post('/users')
async def post_user(schema: User):
    async with in_transaction() as conn:
        unique_id = schema.unique_id
        password = schema.password
        exist = await Users.filter(unique_id=unique_id).first()
        if exist is not None:
            await Users.filter(unique_id=unique_id).update(username=schema.username, password=password,
                                                           unique_id=unique_id, name=schema.name, patch_state=0)
            await UserAuth.filter(user_id=exist.id).delete()
            for state in schema.authority:
                st = await States.filter(unique_id=state.state_unique_id).first()
                auth = UserAuth(user_id=exist.id, state_id=st.id, unique_id=state.unique_id)
                await auth.save(using_db=conn)
            return {
                "success": True
            }
        new = Users(username=schema.username, password=password, unique_id=unique_id, name=schema.name)
        await new.save(using_db=conn)
        for state in schema.authority:
            st = await States.filter(unique_id=state.state_unique_id).first()
            auth = UserAuth(user_id=new.id, state_id=st.id, unique_id=state.unique_id)
            await auth.save(using_db=conn)
    return {
        "success": True
    }


# receive Installments new adding 'POST' or edit
@general_router.post('/installments')
async def add_installments(schema: Installment):
    if schema.patch is True:
        await Installments.filter(unique_id=schema.unique_id).delete()
    stu_installments = await Installments.filter(unique_id=schema.unique_id).all()
    for unique in stu_installments:
        if unique.unique_id == schema.unique_id:
            return {
                False
            }
    async with in_transaction() as conn:
        if schema.patch is True:
            new = Installments(name=schema.name, unique_id=schema.unique_id, patch_state=1)
        else:
            new = Installments(name=schema.name, unique_id=schema.unique_id)
        await new.save(using_db=conn)
    return {
        True
    }


# receive new State 'POST' or edit
@general_router.post('/state')
async def post_institute(schema: State):
    if schema.patch is True:
        await States.filter(unique_id=schema.unique_id).delete()
    stu_states = await States.filter(unique_id=schema.unique_id).all()
    for unique in stu_states:
        if unique.unique_id == schema.unique_id:
            return {
                False
            }
    async with in_transaction() as conn:
        if schema.patch is True:
            new = States(name=schema.name, unique_id=schema.unique_id, patch_state=1)
        else:
            new = States(name=schema.name, unique_id=schema.unique_id)
        await new.save(using_db=conn)
    return {
        True
    }


# receive new student_installment
@general_router.post('/student_installment')
async def post_student_installment(schema: StudentInstallment):
    if schema.patch is True:
        await StudentInstallments.filter(unique_id=schema.unique_id).delete()
    student = await Students.filter(unique_id=schema.student_unique_id).first()
    old_install = await Installments.filter(unique_id=schema.install_unique_id).first()
    async with in_transaction() as conn:
        if schema.patch is True:

            new = StudentInstallments(amount=schema.amount, date=schema.date, installment_id=old_install.id,
                                      invoice=schema.invoice, student_id=student.id,
                                      unique_id=schema.unique_id, patch_state=1)
        else:
            new = StudentInstallments(amount=schema.amount, date=schema.date, installment_id=old_install.id,
                                      invoice=schema.invoice, student_id=student.id,
                                      unique_id=schema.unique_id)
        await new.save(using_db=conn)
    return {
        True
    }


# receive new student
@general_router.post('/student')
async def post_student(schema: Student):
    if schema.patch is True:
        await Students.filter(unique_id=schema.unique_id).delete()
    state_id = await States.filter(unique_id=schema.state_unique_id).first()
    async with in_transaction() as conn:
        if schema.patch is True:
            new = Students(name=schema.name, school=schema.school, branch_id=schema.branch_id,
                           governorate_id=schema.governorate_id, institute_id=schema.institute_id,
                           state_id=state_id.id,
                           first_phone=schema.first_phone, second_phone=schema.second_phone, code_1=schema.code_1,
                           code_2=schema.code_2,
                           telegram_user=schema.telegram_user, created_at=schema.created_at, note=schema.note,
                           total_amount=schema.total_amount, poster_id=schema.poster,
                           remaining_amount=schema.remaining_amount,
                           unique_id=schema.unique_id, patch_state=1
                           )
            await new.save(using_db=conn)
        else:
            new = Students(name=schema.name, school=schema.school, branch_id=schema.branch_id,
                           governorate_id=schema.governorate_id, institute_id=schema.institute_id,
                           state_id=state_id.id,
                           first_phone=schema.first_phone, second_phone=schema.second_phone, code_1=schema.code_1,
                           code_2=schema.code_2,
                           telegram_user=schema.telegram_user, created_at=schema.created_at, note=schema.note,
                           total_amount=schema.total_amount, poster_id=schema.poster,
                           remaining_amount=schema.remaining_amount,
                           unique_id=schema.unique_id
                           )
            await new.save(using_db=conn)
    return {
        True
    }


# receive deleted data
@general_router.post('/del')
async def del_student(schema: Del):
    for unique_id in schema.unique_id_students:
        await Students.filter(unique_id=unique_id).update(delete_state=1)
        stu = await Students.filter(unique_id=unique_id).first()
        if stu is not None:
            await StudentInstallments.filter(student_id=stu.id).update(delete_state=1)
    for unique_id in schema.unique_id_students_install:
        await StudentInstallments.filter(unique_id=unique_id).update(delete_state=1)
    for unique_id in schema.unique_id_states:
        await States.filter(unique_id=unique_id).update(delete_state=1)
        st = await States.filter(unique_id=unique_id).first()
        if st is not None:
            await Students.filter(state_id=st.id).update(delete_state=1)
    for unique_id in schema.unique_id_installment:
        await Installments.filter(unique_id=unique_id).update(delete_state=1)
        inst = await Installments.filter(unique_id=unique_id).first()
        if inst is not None:
            await StudentInstallments.filter(installment_id=inst.id).update(delete_state=1)
    for unique_id in schema.unique_id_users:
        await Users.filter(unique_id=unique_id).update(delete_state=1)
    return {
        True
    }


# to get all students deleted or edited or not
@general_router.get('/students')
async def get_students():
    all_students = await Students.filter().prefetch_related('state').all()
    all_json = []
    for stu in all_students:
        student_json = stu.__dict__
        all_json.append(student_json)
    return {
        "students": all_json
    }


# to get all or patched states
@general_router.get('/states')
async def get_states():
    return {
        "states": await States.all()
    }


# to get all or patched student installment
@general_router.get('/student_installment')
async def get_states():
    query = await StudentInstallments.all().prefetch_related('student', 'installment')
    return {
        "students_installments": [n.__dict__ for n in query]
    }


@general_router.get('/branches')
async def get_branches():
    return {
        "branches": await Branches.all()
    }


@general_router.get('/governorates')
async def get_governorates():
    return {
        "governorates": await Governorates.all()
    }


@general_router.get('/installments')
async def get_installments():
    return {
        "installments": await Installments.all()
    }


@general_router.get('/institutes')
async def get_institutes():
    return {
        "institutes": await Institutes.all()
    }


@general_router.get('/posters')
async def get_posters():
    return {
        "posters": await Posters.all()
    }
