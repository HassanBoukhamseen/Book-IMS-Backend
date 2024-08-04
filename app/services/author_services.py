from sqlalchemy import select, update, delete
from app.database.connector import connect_to_db
from app.database.schemas.author import Author
# from app.database.schemas.book_author import BookAuthor
from app.schemas.author import Author as pydantic_author
from app.schemas.author import AuthorUpdateCurrent


def retrieve_single_author(id):
    try:
        engine, session = connect_to_db()
        stmt = select(Author.author_id, Author.name, Author.biography).where(Author.author_id == id)
        with engine.connect() as conn:
            results = conn.execute(stmt)
            output = results.fetchone()
            if output:
                author = {"author_id": output[0], "name": output[1], "biography": output[2]}
                return True, "Author successfully retrieved", author
            else:
                return False, "Author could not be retrieved", None
    except Exception as e:
        return False, e, None
    finally:
        session.close()

def retrieve_authors_from_db(page: int = 1, per_page: int = 10):
    try:
        engine, session = connect_to_db()
        offset = (page - 1) * per_page
        stmt = select(Author.author_id, Author.name, Author.biography).offset(offset).limit(per_page)
        with engine.connect() as conn:
            results = conn.execute(stmt)
            authors = [{"author_id": result[0], "name": result[1], "biography": result[2]} for result in results.fetchall()]
        return True, "Authors successfully retrieved", authors
    except Exception as e:
        return False, e, None
    finally:
        session.close()

    
def add_author_to_database(author: pydantic_author):
    engine, session = connect_to_db()
    stmt_check_author_exists = select(Author.author_id).where(Author.author_id == author.author_id)
    stmt_add_author = Author(
        name=author.name,
        biography=author.biography
    )
    try:
        with engine.connect() as conn:
            results = conn.execute(stmt_check_author_exists)
            output = results.fetchone()
            session.add(stmt_add_author)
            session.commit()
            author_id = stmt_add_author.author_id
            return True, "Author added successfuly", author_id
    except Exception as e:
        print(e)
        return False, e, None
    finally:
        session.close()

def edit_author_info(author_id: int, new_author: AuthorUpdateCurrent):
    success, message, author = retrieve_single_author(author_id)
    if not success:
        return success, message
    
    updated_user_data = {
        "name": new_author.name if new_author.name is not None else author['name'],
        "biography": new_author.biography if new_author.biography is not None else author['biography'],
    }

    stmt = (
        update(Author)
        .where(Author.author_id == author_id)
        .values(
                name=updated_user_data["name"], 
                biography=updated_user_data["biography"]
        )
        .execution_options(synchronize_session="fetch")
    )

    try:
        engine, session = connect_to_db()
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
    except Exception as e:
        return False, e
    finally:
        session.close()
    return True, "Author information successfully changed"

def delete_author_from_db(author_id: int):
    stmt = delete(Author).where(Author.author_id == author_id)
    try:
        engine, session = connect_to_db()
        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
    except Exception as e:
        return False, e
    finally:
        session.close()
    return True, "Author information successfully deleted"

if __name__ == "__main__":
    pass
    
