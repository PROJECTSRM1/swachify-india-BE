# services/companies_service.py

from sqlalchemy import text
from sqlalchemy.orm import Session


def get_all_companies(
    db: Session,
    industry_id: int | None = None,
    company_size_id: int | None = None,
    location: str | None = None,
    sort_by: str | None = None,
):
    """
    Returns company list with job & internship counts.
    Default: returns ALL companies (no filters).
    """

    query = """
        SELECT
            ROW_NUMBER() OVER (ORDER BY MAX(jo.created_date) DESC) AS company_id,
            jo.company_name,
            jo.company_address AS location,

            jo.industry_id,
            mi.industry_name,

            jo.company_size_id,
            mcs.size_range AS company_size,

            COUNT(*) FILTER (
                WHERE jo.is_active = TRUE
                  AND jo.sub_module_id = 1
            ) AS jobs_count,

            COUNT(*) FILTER (
                WHERE jo.is_active = TRUE
                  AND jo.sub_module_id = 2
            ) AS internships_count,

            'Active' AS hiring_status,
            MAX(jo.created_date) AS last_active_time

        FROM job_openings jo
        LEFT JOIN master_industry mi
               ON mi.id = jo.industry_id
        LEFT JOIN master_company_size mcs
               ON mcs.id = jo.company_size_id
        WHERE jo.is_active = TRUE
    """

    params = {}

    # -------------------------
    # OPTIONAL FILTERS
    # -------------------------
    if industry_id:
        query += " AND jo.industry_id = :industry_id"
        params["industry_id"] = industry_id

    if company_size_id:
        query += " AND jo.company_size_id = :company_size_id"
        params["company_size_id"] = company_size_id

    if location:
        query += " AND LOWER(jo.company_address) LIKE :location"
        params["location"] = f"%{location.lower()}%"

    # -------------------------
    # GROUP BY
    # -------------------------
    query += """
        GROUP BY
            jo.company_name,
            jo.company_address,
            jo.industry_id,
            mi.industry_name,
            jo.company_size_id,
            mcs.size_range
    """

    # -------------------------
    # SORTING
    # -------------------------
    if sort_by == "latest":
        query += " ORDER BY last_active_time DESC"
    elif sort_by == "jobs":
        query += " ORDER BY jobs_count DESC"
    elif sort_by == "internships":
        query += " ORDER BY internships_count DESC"
    else:
        # DEFAULT (important)
        query += " ORDER BY last_active_time DESC"

    return db.execute(text(query), params).mappings().all()
