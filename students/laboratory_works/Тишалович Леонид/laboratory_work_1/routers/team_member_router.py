from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException

from repositories.team_member_repository import TeamMemberRepository
from schemas import TeamMemberCreate, TeamMemberUpdate

router = APIRouter(
    prefix="/team-members",
    tags=["Участники команд"]
)


@router.post("/")
async def create_team_member(
        team_member: Annotated[TeamMemberCreate, Depends()]
):
    await TeamMemberRepository.create(team_member)


@router.get("/")
async def get_all_team_members() -> List[TeamMemberCreate]:
    return await TeamMemberRepository.get_all()


@router.get("/{team_member_id}")
async def get_team_member(team_member_id: int) -> TeamMemberCreate:
    team_member = await TeamMemberRepository.get_by_id(team_member_id)
    if not team_member:
        raise HTTPException(status_code=404, detail="Team member not found")
    return team_member


@router.put("/{team_member_id}")
async def update_team_member(team_member_id: int, team_member_data: TeamMemberUpdate):
    updated_team_member = await TeamMemberRepository.update(team_member_id, team_member_data)
    if not updated_team_member:
        raise HTTPException(status_code=404, detail="Team member not found")
    return updated_team_member


@router.delete("/{team_member_id}")
async def delete_team_member(team_member_id: int):
    deleted_team_member = await TeamMemberRepository.delete(team_member_id)
    if not deleted_team_member:
        raise HTTPException(status_code=404, detail="Team member not found")
    return {"message": "Team member deleted successfully"}
