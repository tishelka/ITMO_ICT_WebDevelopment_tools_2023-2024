from sqlalchemy.orm import Session
from fastapi import HTTPException

from database import SessionLocal
from schemas import SubmissionCreate, Submission, SubmissionUpdate


class SubmissionRepository:
    @classmethod
    async def create(cls, data: SubmissionCreate):
        with SessionLocal() as session:
            submission_dict = data.model_dump()

            if submission_dict:
                try:
                    submission = Submission(**submission_dict)
                    session.add(submission)
                    session.commit()
                    return submission
                except Exception as e:
                    session.rollback()
                    raise HTTPException(status_code=500, detail=str(e))
            else:
                raise HTTPException(status_code=400, detail="Invalid data provided")

    @classmethod
    async def get_all(cls):
        with SessionLocal() as session:
            return session.query(Submission).all()

    @classmethod
    async def get_by_id(cls, submission_id: int):
        with SessionLocal() as session:
            return session.query(Submission).filter(Submission.id == submission_id).first()

    @classmethod
    async def update(cls, submission_id: int, submission_data: SubmissionUpdate):
        with SessionLocal() as session:
            submission = session.query(Submission).filter(Submission.id == submission_id).first()
            if submission:
                for field, value in submission_data.dict().items():
                    setattr(submission, field, value)
                session.commit()
                return submission
            else:
                return None

    @classmethod
    async def delete(cls, submission_id: int):
        with SessionLocal() as session:
            submission = session.query(Submission).filter(Submission.id == submission_id).first()
            if submission:
                session.delete(submission)
                session.commit()
                return submission
            else:
                return None
