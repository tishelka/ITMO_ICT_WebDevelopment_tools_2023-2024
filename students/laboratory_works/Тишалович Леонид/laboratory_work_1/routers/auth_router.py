from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
from utils.auth_utils import create_access_token, verify_password
from database import SessionLocal
from schemas import ParticipantCreate, Participant
from typing import Annotated
from repositories.participant_repository import ParticipantRepository

router = APIRouter(prefix="", tags=["Аутентификация"])


@router.post("/register/", response_model=schemas.ParticipantCreate)
async def register(participant: Annotated[ParticipantCreate, Depends()]):
    return await ParticipantRepository.create_with_token(participant)


@router.post("/login/")
async def login(email: str, password: str):
    participant = await ParticipantRepository.authenticate(email, password)
    if not participant:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    access_token = create_access_token(data={"sub": participant.email})
    return {"access_token": access_token, "token_type": "bearer"}
