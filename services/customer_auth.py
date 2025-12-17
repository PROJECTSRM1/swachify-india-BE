from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from controllers.user_controller import register_user_controller
from utils.sms_agent import send_welcome_sms


def register_user_service(
    db: Session,
    payload,
    background_tasks: BackgroundTasks
):
    """
    Handles:
    - DB registration
    - Background notifications
    """

    # 1️⃣ Register user (DB only)
    user = register_user_controller(db, payload)

    # 2️⃣ Background SMS (non-blocking)
    background_tasks.add_task(
        send_welcome_sms,
        payload.mobile,
        payload.first_name
    )

    return user
