from sqlalchemy.orm import Session
# from models.master_module import MasterModule
# from models.user_services import UserServices
# from models.user_registration import UserRegistration

from models.generated_models import MasterModule, UserServices, UserRegistration


def get_dashboard(db: Session, user: UserRegistration):

    user_modules = (
        db.query(MasterModule)
        .join(UserServices, UserServices.module_id == MasterModule.id)
        .filter(
            UserServices.user_id == user.id,
            MasterModule.is_active.is_(True)
        )
        .all()
    )

    categories = [
        {
            "id": m.id,
            "title": m.module_name,
            "enabled": True
        }
        for m in user_modules
    ]

    return {
        "user": {
            "user_id": user.id,
            "name": f"{user.first_name} {user.last_name or ''}".strip(),
            "role_id": user.role_id,
            "status_id": user.status_id
        },
         "dashboard_flags": {
            "approval_pending": user.status_id == 2,
            "can_book_service": user.role_id == 2,  # Customers can book services
            "can_accept_jobs": user.role_id == 4 and user.status_id == 1  # Only approved freelancers can accept jobs
        },
        "categories": categories
    }
