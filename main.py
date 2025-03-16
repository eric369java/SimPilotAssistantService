from typing import Annotated
from uuid import UUID
import logging;

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, create_engine, select

from models import Aircraft, Checklist_Item

uvicorn_error = logging.getLogger("uvicorn.access")
uvicorn_error.disabled = True

connect_args = {"check_same_thread": False}
engine = create_engine('postgresql+psycopg2://dev:eliu369db@127.0.0.1:5433/sim_pilot_assistant')

def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db()


@app.get("/aircrafts/")
def read_aircrafts(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Aircraft]:
    aircrafts = session.exec(select(Aircraft).offset(offset).limit(limit)).all()
    return aircrafts


@app.get("/aircrafts/{aircraft_path_param}/checklist-items/")
def read_checklist_items(aircraft_path_param: str, session: SessionDep, offset : int = 0, limit : int = 50) -> list[Checklist_Item]:
    aircraft_id = UUID(aircraft_path_param)
    checklist_items = session.exec(select(Checklist_Item).where(Checklist_Item.aircraft_id == aircraft_id).order_by(Checklist_Item.item_order).offset(offset).limit(limit))
    return checklist_items