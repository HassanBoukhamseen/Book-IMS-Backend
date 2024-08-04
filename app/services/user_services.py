from sqlalchemy import select, update
from app.database.connector import connect_to_db
from app.database.schemas.user import User
from app.utils.hash import deterministic_hash


def retrieve_all_users():
    try:
        engine, session = connect_to_db()
        stmt = select(User)
        with engine.connect() as conn:
            results = conn.execute(stmt)
            outputs = results.fetchall()
            if outputs is not None:
                users = [{
                    "email": output[0],
                    "fname": output[1],
                    "lname": output[2],
                    "role": output[3],
                    "password": output[4]
                } for output in outputs]
                return True, "Users retrieved sucessfully", users
            else:
                return False, "Users not found", None
    except Exception as e:
        return False, e, None
    finally:
        session.close()

def retrieve_single_user(id):
    try:
        engine, session = connect_to_db()
        stmt = select(User.email, User.fname, User.lname, User.role, User.hashed_pw).where(User.email == id)
        with engine.connect() as conn:
            results = conn.execute(stmt)
            output = results.fetchone()
            if output is not None:
                user = {
                    "email": output[0],
                    "fname": output[1],
                    "lname": output[2],
                    "role": output[3],
                    "password": output[4]
                }
                return True, "User retrieved sucessfully", user
            else:
                return False, "User not found", None
    except Exception as e:
        return False, e, None
    finally:
        session.close()

def edit_user_info(email, user_update):
    success, message, user = retrieve_single_user(email)
    if not success:
        return success, message
    
    updated_user_data = {
        "fname": user_update.fname if user_update.fname is not None else user['fname'],
        "lname": user_update.lname if user_update.lname is not None else user['lname'],
        "password": deterministic_hash(user_update.password) if user_update.password is not None else user['password'],
        "role": user['role']
    }

    stmt = (
        update(User)
        .where(User.email == email)
        .values(
                fname=updated_user_data["fname"], 
                lname=updated_user_data["lname"], 
                hashed_pw=updated_user_data["password"], 
                role=updated_user_data["role"])
        .execution_options(synchronize_session="fetch")
    )
 
    try:
        engine, session = connect_to_db()
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
        return True, "User updated successfully"
    except Exception as e:
        print(e)
        return False, e
    finally:
        session.close()

def register_user(user_data):
    try:
        engine, session = connect_to_db()
        select_user_email = select(User.email).where(User.email == user_data.email)
        with engine.connect() as conn:
            results = conn.execute(select_user_email)
            output = results.fetchone()
            if output is not None:
                return False, "User already registered"
        hashed_pw = deterministic_hash(user_data.hashedpw)
        new_user = User(
            email=user_data.email,
            fname=user_data.fname,
            lname=user_data.lname,
            hashed_pw=hashed_pw,
            role=user_data.role
        )
        session.add(new_user)
        session.commit()
        return True, "User registered successfully"
    except Exception as e:
        return False, e
    finally:
        session.close()

def authenticate_user(email, password):
    try:
        engine, session = connect_to_db()
        stmt = select(User.hashed_pw).where(User.email == email)
        with engine.connect() as conn:
            results = conn.execute(statement=stmt)
            output = results.fetchone()
            if output is None:
                return False, "User not registered"
            else:
                print(output[0], deterministic_hash(password))
                if output[0] == deterministic_hash(password):
                    return True, "Login successful"
                else:
                    return False, "Wrong password"
    except Exception as e:
        return False, e
    finally:
        session.close()    