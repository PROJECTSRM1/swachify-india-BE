from sqlalchemy.orm import Session
from sqlalchemy import text

def get_all_home_services(db: Session):
    query = text("""
        SELECT *
        FROM vw_home_service_booking_summary
        ORDER BY id DESC
    """)

    return db.execute(query).mappings().all()
