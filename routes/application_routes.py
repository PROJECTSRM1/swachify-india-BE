from fastapi import APIRouter,HTTPException
from schemas.application_schema import ApplicationUpdateRequest,ApplicationReviewResponse
from services.application_service import get_application_review, update_application

router = APIRouter(prefix="/internship/application", tags=["Internship Application"])




@router.get(
    "/{user_id}",
    response_model=ApplicationReviewResponse
)
def get_application(user_id: int):
    data = get_application_review(user_id)

    if not data:
        raise HTTPException(status_code=404, detail="User not found")

    return data


@router.put("/{user_id}")
def update_application_api(user_id: int, payload: ApplicationUpdateRequest):
    update_application(user_id, payload)
    return {"message": "Updated successfully"}