from sqlalchemy.orm import Session
from models.user_registration import UserRegistration


# ---------------------------------------------------------
# REGISTER FREELANCER
# ---------------------------------------------------------
def freelancer_register_service(data, db: Session):
    new_freelancer = UserRegistration(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        mobile=data.mobile,
        role_id=4   # freelancer role
    )
    db.add(new_freelancer)
    db.commit()
    db.refresh(new_freelancer)
    return new_freelancer


# ---------------------------------------------------------
# LOGIN FREELANCER
# ---------------------------------------------------------
def freelancer_login_service(data, db: Session):
    freelancer = (
        db.query(UserRegistration)
        .filter(UserRegistration.email == data.email,
                UserRegistration.role_id == 4)
        .first()
    )
    return freelancer


# ---------------------------------------------------------
# UPDATE FREELANCER
# ---------------------------------------------------------
def freelancer_update_service(freelancer_id: int, data, db: Session):
    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == 4
    ).first()

    if not freelancer:
        return None

    for key, value in data.dict().items():
        setattr(freelancer, key, value)

    db.commit()
    db.refresh(freelancer)
    return freelancer


# ---------------------------------------------------------
# DELETE (SOFT DELETE)
# ---------------------------------------------------------
def freelancer_delete_service(freelancer_id: int, db: Session):
    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == 4
    ).first()

    if not freelancer:
        return None

    freelancer.is_active = False
    db.commit()
    return freelancer


# ---------------------------------------------------------
# HARD DELETE
# ---------------------------------------------------------
def freelancer_hard_delete_service(freelancer_id: int, db: Session):
    freelancer = db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == 4
    ).first()

    if not freelancer:
        return None

    db.delete(freelancer)
    db.commit()
    return True


# ---------------------------------------------------------
# GET ALL FREELANCERS
# ---------------------------------------------------------
def get_all_freelancers_service(db: Session):
    return db.query(UserRegistration).filter(
        UserRegistration.role_id == 4
    ).all()


# ---------------------------------------------------------
# GET ONE FREELANCER
# ---------------------------------------------------------
def get_freelancer_by_id_service(freelancer_id: int, db: Session):
    return db.query(UserRegistration).filter(
        UserRegistration.id == freelancer_id,
        UserRegistration.role_id == 4
    ).first()
