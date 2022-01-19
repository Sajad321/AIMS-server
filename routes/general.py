from fastapi import APIRouter

general_router = APIRouter()


# receive bulky new adding 'POST'
@general_router.post('/add')
async def add():
    return {

    }
