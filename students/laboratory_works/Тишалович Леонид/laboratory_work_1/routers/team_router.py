from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from repositories.team_repository import TeamRepository
from repositories.team_member_repository import TeamMemberRepository
from schemas import TeamCreate, TeamUpdate, TeamMemberCreate
from utils.auth_utils import get_user_from_token

router = APIRouter(
    prefix="/teams",
    tags=["Команды"]
)


@router.post("/")
async def create_team(
        team: Annotated[TeamCreate, Depends()]
):
    await TeamRepository.create(team)


@router.get("/")
async def get_all_teams() -> List[TeamCreate]:
    return await TeamRepository.get_all()


@router.get("/{team_id}")
async def get_team(team_id: int) -> TeamCreate:
    team = await TeamRepository.get_by_id(team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.put("/{team_id}")
async def update_team(team_id: int, team_data: TeamUpdate):
    updated_team = await TeamRepository.update(team_id, team_data)
    if not updated_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return updated_team


@router.delete("/{team_id}")
async def delete_team(team_id: int):
    deleted_team = await TeamRepository.delete(team_id)
    if not deleted_team:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"message": "Team deleted successfully"}


@router.post("/{team_id}/add_member/")
async def add_member_to_team(
        team_id: int,
        team_member: Annotated[TeamMemberCreate, Depends()]
):
    team_member.team_id = team_id
    await TeamMemberRepository.create(team_member)
    return {"message": "Member added to team successfully"}
