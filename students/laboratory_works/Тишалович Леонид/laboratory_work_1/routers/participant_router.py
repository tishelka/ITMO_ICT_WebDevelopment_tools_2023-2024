from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from repositories.participant_repository import ParticipantRepository
from schemas import ParticipantCreate, ParticipantUpdate

router = APIRouter(prefix="/participants", tags=["Участники"])


@router.post("/")
async def create_participant(
        participant: Annotated[ParticipantCreate, Depends()]
):
    await ParticipantRepository.create(participant)


@router.get("/")
async def get_all_participants() -> list[ParticipantCreate]:
    return await ParticipantRepository.get_all()


@router.get("/{participant_id}")
async def get_participant(participant_id: int) -> ParticipantCreate:
    participant = await ParticipantRepository.get_by_id(participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant


@router.put("/{participant_id}")
async def update_participant(participant_id: int, participant_data: ParticipantUpdate):
    updated_participant = await ParticipantRepository.update(participant_id, participant_data)
    if not updated_participant:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_participant


@router.delete("/{participant_id}")
async def delete_participant(participant_id: int):
    deleted_participant = await ParticipantRepository.delete(participant_id)
    if not deleted_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return {"message": "Participant deleted successfully"}
