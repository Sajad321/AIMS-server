from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.general import general_router


def create_app() -> FastAPI:
    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_tortoise(
        app,
        db_url='postgres://zjrjzsjqskajpx:8c61868cef47cf6f885ca90ac167023e0a06cb3537986834636eda039f28b6e3@ec2-3-212-143-188.compute-1.amazonaws.com:5432/dc1nmtqmk06hbn',
        modules={'models': ["models.models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    register_views(app=app)
    return app


def register_views(app: FastAPI):
    app.include_router(general_router, tags=["General"])


TORTOISE_ORM = {
    "connections": {
        "default": "postgres://zjrjzsjqskajpx:8c61868cef47cf6f885ca90ac167023e0a06cb3537986834636eda039f28b6e3@ec2-3-212-143-188.compute-1.amazonaws.com:5432/dc1nmtqmk06hbn"
    },
    "apps": {
        "models": {
            "models": [
                "models.models", "aerich.models"
            ],
            "default_connection": "default",
        },
    },
}
