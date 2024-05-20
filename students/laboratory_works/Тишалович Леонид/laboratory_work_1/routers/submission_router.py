from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from repositories.submission_repository import SubmissionRepository
from schemas import SubmissionCreate, SubmissionUpdate

router = APIRouter(
    prefix="/submissions",
    tags=["Заявки на задания"]
)


@router.post("/")
async def create_submission(
        submission: Annotated[SubmissionCreate, Depends()]
):
    await SubmissionRepository.create(submission)


@router.get("/")
async def get_all_submissions() -> List[SubmissionCreate]:
    return await SubmissionRepository.get_all()


@router.get("/{submission_id}")
async def get_submission(submission_id: int) -> SubmissionCreate:
    submission = await SubmissionRepository.get_by_id(submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return submission


@router.put("/{submission_id}")
async def update_submission(submission_id: int, submission_data: SubmissionUpdate):
    updated_submission = await SubmissionRepository.update(submission_id, submission_data)
    if not updated_submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return updated_submission


@router.delete("/{submission_id}")
async def delete_submission(submission_id: int):
    deleted_submission = await SubmissionRepository.delete(submission_id)
    if not deleted_submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {"message": "Submission deleted successfully"}


@router.post("/{submission_id}/evaluate/")
async def evaluate_submission(submission_id: int, evaluation: str):
    submission = await SubmissionRepository.get_by_id(submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    submission.evaluation = evaluation
    await SubmissionRepository.update(submission_id, submission)
    return {"message": "Submission evaluated successfully"}
