from sqlalchemy import text
from sqlalchemy.orm import Session

def execute_create_user_function(db, params):
    try:
        query = text("""
            SELECT * FROM fn_create_user_list(
                :p_first_name,
                :p_last_name,
                :p_email,
                :p_mobile,
                :p_password,
                :p_gender_id,
                :p_unique_id,
                :p_dob,
                :p_age,
                :p_role_id,
                :p_state_id,
                :p_district_id,
                :p_created_by,
                :p_profile_image,
                :p_skill_id,
                :p_experience_summary,
                :p_experience_doc,
                :p_government_id
            );
        """)

        result = db.execute(query, params).fetchone()
        db.commit()
        return result

    except Exception as e:
        db.rollback()
        raise e


def execute_function_raw(db, query, params):
    try:
        result = db.execute(text(query), params).fetchone()
        db.commit()

        if not result:
            return None

        return dict(result._mapping)   # <--- guaranteed keys
    except Exception as e:
        db.rollback()
        raise e

