from sqlalchemy.orm import Session
from sqlalchemy import text

# ======================================================
# HOME SERVICE BOOKING SUMMARY (VIEW)
# ======================================================

def get_home_service_booking_summary(
    db: Session,
    institution_id: int = -1
):
    """
    Fetch data from vw_home_service_booking_summary
    - institution_id = -1 → fetch all
    """

    query = text("""
        SELECT *
        FROM vw_home_service_booking_summary
        WHERE (:institution_id = -1 OR institution_id = :institution_id)
    """)

    result = db.execute(
        query,
        {
            "institution_id": institution_id
        }
    )

    return result.mappings().all()
