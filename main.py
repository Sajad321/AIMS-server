import uvicorn
from starlette.middleware.gzip import GZipMiddleware

from config import create_app
from models.models import Students, StudentInstallments

app = create_app()

app.add_middleware(GZipMiddleware)


@app.get('/students')
async def get_students():
    all_students = await Students.filter().prefetch_related('state').all()
    all_json = []
    for stu in all_students:
        student_json = stu.__dict__
        all_json.append(student_json)
    return {
        "students": all_json
    }


# to get all or patched student installment
@app.get('/student_installment')
async def get_states():
    query = await StudentInstallments.all().prefetch_related('student', 'installment')
    return {
        "students_installments": [n.__dict__ for n in query]
    }
