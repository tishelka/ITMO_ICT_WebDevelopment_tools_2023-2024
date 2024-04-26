from fastapi import HTTPException

from database import SessionLocal
from schemas import ParticipantCreate, Participant, ParticipantUpdate
from utils.auth_utils import create_access_token, verify_password


class ParticipantRepository:
    @classmethod
    async def create_with_token(cls, data: ParticipantCreate):
        with SessionLocal() as session:
            participant_dict = data.dict()
            participant = Participant(**participant_dict)
            participant.set_password(data.password)
            session.add(participant)
            session.commit()
            access_token = create_access_token(data={"sub": participant.email})
            return ParticipantCreate(**participant_dict, access_token=access_token)

    @classmethod
    async def authenticate(cls, email: str, password: str):
        with SessionLocal() as session:
            participant = session.query(Participant).filter(Participant.email == email).first()
            if not participant or not verify_password(password, participant.password):
                return None
            return participant

    @classmethod
    async def create(cls, data: ParticipantCreate):
        with SessionLocal() as session:
            participant_dict = data.model_dump()

            if participant_dict:
                try:
                    participant = Participant(**participant_dict)
                    session.add(participant)
                    session.commit()

                    return participant
                except Exception as e:
                    session.rollback()
                    raise HTTPException(status_code=500, detail=str(e))
            else:
                raise HTTPException(status_code=400, detail="Invalid data provided")

    @classmethod
    async def get_all(cls):
        with SessionLocal() as session:
            return session.query(Participant).all()

    @classmethod
    async def get_by_id(cls, participant_id: int):
        with SessionLocal() as session:
            return session.query(Participant).filter(Participant.id == participant_id).first()

    @classmethod
    async def update(cls, participant_id: int, participant_data: ParticipantUpdate):
        with SessionLocal() as session:
            participant = session.query(Participant).filter(Participant.id == participant_id).first()
            if participant:
                for field, value in participant_data.dict().items():
                    setattr(participant, field, value)
                session.commit()
                return participant
            else:
                return None

    @classmethod
    async def delete(cls, participant_id: int):
        with SessionLocal() as session:
            participant = session.query(Participant).filter(Participant.id == participant_id).first()
            if participant:
                session.delete(participant)
                session.commit()
                return participant
            else:
                return None
