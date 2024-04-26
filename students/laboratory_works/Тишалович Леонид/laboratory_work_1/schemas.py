from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
from utils.auth_utils import get_password_hash


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    contact_number = Column(String)
    registration_date = Column(DateTime, default=func.now())
    password = Column(String)

    def set_password(self, password: str):
        self.password = get_password_hash(password)


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    creation_date = Column(DateTime, default=func.now())


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, ForeignKey("participants.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))

    participant = relationship("Participant", back_populates="teams")
    team = relationship("Team", back_populates="members")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    requirements = Column(String)
    evaluation_criteria = Column(String)
    publication_date = Column(DateTime, default=func.now())


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    work_link = Column(String)
    submission_date = Column(DateTime, default=func.now())

    task = relationship("Task", back_populates="submissions")
    team = relationship("Team", back_populates="submissions")


Participant.teams = relationship("TeamMember", back_populates="participant")
Team.members = relationship("TeamMember", back_populates="team")
Task.submissions = relationship("Submission", back_populates="task")
Team.submissions = relationship("Submission", back_populates="team")

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str
    description: str
    requirements: str
    evaluation_criteria: str


class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    requirements: str = None
    evaluation_criteria: str = None


class ParticipantCreate(BaseModel):
    name: str
    email: str
    contact_number: str
    password: str


class ParticipantResponse(BaseModel):
    name: str
    email: str
    contact_number: str


class ParticipantUpdate(BaseModel):
    name: str = None
    email: str = None
    contact_number: str = None


class TeamCreate(BaseModel):
    name: str
    description: str


class TeamUpdate(BaseModel):
    name: str = None
    description: str = None


class TeamMemberCreate(BaseModel):
    participant_id: int
    team_id: int


class TeamMemberUpdate(BaseModel):
    participant_id: int = None
    team_id: int = None


class SubmissionCreate(BaseModel):
    task_id: int
    team_id: int
    work_link: str


class SubmissionUpdate(BaseModel):
    task_id: int = None
    team_id: int = None
    work_link: str = None
