from fastapi import APIRouter, HTTPException
from repositories.team_member_repository import TeamMemberRepository, TeamMember
from schemas import TeamMemberCreate
from typing import List

router = APIRouter()

team_member_repo = TeamMemberRepository()


@router.post("/", response_model=TeamMember)
def create_team_member(team_member: TeamMemberCreate):
    new_team_member = TeamMember(id=len(team_member_repo.team_members) + 1, **team_member.dict())
    team_member_repo.add(new_team_member)
    return new_team_member


@router.get("/{team_member_id}", response_model=TeamMember)
def read_team_member(team_member_id: int):
    team_member = team_member_repo.get(team_member_id)
    if team_member is None:
        raise HTTPException(status_code=404, detail="Team member not found")
    return team_member


@router.get("/team/{team_id}", response_model=List[TeamMember])
def read_team_members_by_team(team_id: int):
    return team_member_repo.get_by_team(team_id)


@router.get("/participant/{participant_id}", response_model=List[TeamMember])
def read_team_members_by_participant(participant_id: int):
    return team_member_repo.get_by_participant(participant_id)


@router.delete("/{team_member_id}", response_model=TeamMember)
def delete_team_member(team_member_id: int):
    team_member = team_member_repo.get(team_member_id)
    if team_member is None:
        raise HTTPException(status_code=404, detail="Team member not found")
    team_member_repo.remove(team_member_id)
    return team_member


@router.post("/add_to_team", response_model=TeamMember)
def add_participant_to_team(team_id: int, participant_id: int):
    new_team_member = TeamMember(id=len(team_member_repo.team_members) + 1, team_id=team_id, participant_id=participant_id)
    team_member_repo.add(new_team_member)
    return new_team_member


@router.delete("/remove_from_team", response_model=TeamMember)
def remove_participant_from_team(team_id: int, participant_id: int):
    team_members = team_member_repo.get_by_team(team_id)
    for team_member in team_members:
        if team_member.participant_id == participant_id:
            team_member_repo.remove(team_member.id)
            return team_member
    raise HTTPException(status_code=404, detail="Team member not found")
