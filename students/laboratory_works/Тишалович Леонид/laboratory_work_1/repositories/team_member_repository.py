from sqlalchemy.orm import Session
from fastapi import HTTPException

from database import SessionLocal
from schemas import TeamMemberCreate, TeamMember, TeamMemberUpdate


class TeamMemberRepository:
    @classmethod
    async def create(cls, data: TeamMemberCreate):
        with SessionLocal() as session:
            team_member_dict = data.model_dump()

            if team_member_dict:
                try:
                    team_member = TeamMember(**team_member_dict)
                    session.add(team_member)
                    session.commit()
                    return team_member
                except Exception as e:
                    session.rollback()
                    raise HTTPException(status_code=500, detail=str(e))
            else:
                raise HTTPException(status_code=400, detail="Invalid data provided")

    @classmethod
    async def get_all(cls):
        with SessionLocal() as session:
            return session.query(TeamMember).all()

    @classmethod
    async def get_by_id(cls, team_member_id: int):
        with SessionLocal() as session:
            return session.query(TeamMember).filter(TeamMember.id == team_member_id).first()

    @classmethod
    async def update(cls, team_member_id: int, team_member_data: TeamMemberUpdate):
        with SessionLocal() as session:
            team_member = session.query(TeamMember).filter(TeamMember.id == team_member_id).first()
            if team_member:
                for field, value in team_member_data.dict().items():
                    setattr(team_member, field, value)
                session.commit()
                return team_member
            else:
                return None

    @classmethod
    async def delete(cls, team_member_id: int):
        with SessionLocal() as session:
            team_member = session.query(TeamMember).filter(TeamMember.id == team_member_id).first()
            if team_member:
                session.delete(team_member)
                session.commit()
                return team_member
            else:
                return None
