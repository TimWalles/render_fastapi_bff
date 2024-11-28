from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from src.routers import auth, data, user
from src.services.data_database.engine import init_db
from src.services.user_database.engine import init_user_db
from src.settings import get_settings


async def lifespan(app: FastAPI):
    await init_user_db(settings=get_settings())
    await init_db(settings=get_settings())
    yield


origins = [
    "http://localhost:5173",
    "https://localhost:5173",
    "http://localhost",
    "localhost:5173",
]


# region app
app = FastAPI(lifespan=lifespan)
add_pagination(app)

# region cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(data.router)
