from sqlalchemy.orm import Session
from fastapi import HTTPException

from database import SessionLocal
from schemas import TeamCreate, Team, TeamUpdate


class TeamRepository:
    @classmethod
    async def create(cls, data: TeamCreate):
        with SessionLocal() as session:
            team_dict = data.model_dump()

            if team_dict:
                try:
                    team = Team(**team_dict)
                    session.add(team)
                    session.commit()
                    return team
                except Exception as e:
                    session.rollback()
                    raise HTTPException(status_code=500, detail=str(e))
            else:
                raise HTTPException(status_code=400, detail="Invalid data provided")

    @classmethod
    async def get_all(cls):
        with SessionLocal() as session:
            return session.query(Team).all()

    @classmethod
    async def get_by_id(cls, team_id: int):
        with SessionLocal() as session:
            return session.query(Team).filter(Team.id == team_id).first()

    @classmethod
    async def update(cls, team_id: int, team_data: TeamUpdate):
        with SessionLocal() as session:
            team = session.query(Team).filter(Team.id == team_id).first()
            if team:
                for field, value in team_data.dict().items():
                    setattr(team, field, value)
                session.commit()
                return team
            else:
                return None

    @classmethod
    async def delete(cls, team_id: int):
        with SessionLocal() as session:
            team = session.query(Team).filter(Team.id == team_id).first()
            if team:
                session.delete(team)
                session.commit()
                return team
            else:
                return None
