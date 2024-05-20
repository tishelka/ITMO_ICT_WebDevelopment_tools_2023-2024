from fastapi import FastAPI, Depends
from typing import Annotated
import schemas
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from routers.task_router import router as tasks_router
from routers.participant_router import router as participant_router
from routers.submission_router import router as submission_router
from routers.team_member_router import router as team_member_router
from routers.team_router import router as team_router
from routers.auth_router import router as auth_router

app = FastAPI()
schemas.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
app.include_router(task_router, prefix="/tasks")
app.include_router(participant_router, prefix="/participants")
app.include_router(submission_router, prefix="/submissions")
app.include_router(team_member_router, prefix="/team_members")
app.include_router(team_router, prefix="/teams")
app.include_router(auth_router, prefix="/auth")

