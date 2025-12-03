from sqlalchemy import text
from sqlalchemy.orm import Session


def execute_create_user_function(db: Session, params: dict):
    try:
        query = text("""
            SELECT * FROM fn_create_user_list(
                :p_first_name,
                :p_last_name,
                :p_email,
                :p_mobile,
                :p_password,
                :p_gender_id,
                :p_address
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

        return dict(result._mapping)  
    except Exception as e:
        db.rollback()
        raise e

