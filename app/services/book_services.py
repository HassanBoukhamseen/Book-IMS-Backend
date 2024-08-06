from sqlalchemy import select, delete, insert, update, desc, asc, func, or_
from app.database.connector import connect_to_db
from app.database.schemas.books import Book
from app.database.schemas.preferences import Preferences
from app.database.schemas.book_author import BookAuthor
from app.database.schemas.liked_books import LikedBooks
from app.database.schemas.user import User
from app.database.schemas.author import Author
from app.services.author_services import retrieve_single_author
from app.schemas.book import BookUpdateCurrent
from sqlalchemy import func

order_by_map = {
    "trending": [desc(Book.rating), desc(Book.ratings_count)],
    "publish_year_asc": [asc(Book.year)],
    "publish_year_desc": [desc(Book.year)],
    "average_rating_asc": [asc(Book.rating)],
    "average_rating_desc": [desc(Book.rating)]
}
def retrieve_liked_books_for_user(email: str, start: int = 0, end: int = 12):
    engine, session = connect_to_db()
    try:
        success, message, liked_books_ids = retrieve_liked_books(email)
        if success:
            if liked_books_ids:
                stmt = session.query(Book).filter(Book.book_id.in_(liked_books_ids))
                parsed_results = [{
                    "book_id": row.book_id,
                    "title": row.title,
                    "author_name": row.author_name,
                    "subtitle": row.subtitle,
                    "thumbnail": row.thumbnail,
                    "genre": row.genre,
                    "description": row.description,
                    "year": row.year,
                    "average_rating": row.rating,
                    "num_pages": row.num_pages,
                    "ratings_count": row.ratings_count,
                    "liked": 1
                } for row in stmt.offset(start).limit(end - start)]
                return True, "Books retrieved successfully", parsed_results, stmt.count()
            else:
                return False, "No liked books found for the user", None, 0
        else:
            return False, message, None, 0
    except Exception as e:
        return False, str(e), None, 0
    finally:
        session.close()




def register_liked_book(book_id: str, email: str):
    engine, session = connect_to_db()
    try:
        with engine.connect() as conn:
            stmt = insert(LikedBooks).values(email=email, book_id=book_id)
            conn.execute(stmt)
            conn.commit()
            return True, "Liked Book Added Successfully"
    except Exception as e:
        print(e)
        return False, str(e)
    finally:
        session.close()

def remove_liked_book(book_id: str, email: str):
    engine, session = connect_to_db()
    try:
        with engine.connect() as conn:
            stmt = delete(LikedBooks).where(LikedBooks.email==email, LikedBooks.book_id == book_id)
            conn.execute(stmt)
            conn.commit()
            return True, "Liked Book removed successfully"
    except Exception as e:
        return False, str(e)
    finally:
        session.close()

def retrieve_liked_books(email: str):
    engine, session = connect_to_db()
    try:
        with engine.connect() as conn:
            stmt = select(LikedBooks.book_id).where(LikedBooks.email==email)
            query = conn.execute(stmt)
            results = query.fetchall()
            if results:
                results = [result[0] for result in results]
                return True, "Liked book retrieved successfully", results
            else:
                return False, "Could not retrieved books", None
    except Exception as e:
        return False, str(e), None
    finally:
        session.close()

def parse_output(db_output):
    if db_output is None:
        return None
    books = [{
                "book_id": result[0], 
                "title": result[1], 
                "author_name": result[2],
                "subtitle": result[3],
                "thumbnail": result[4],
                "genre": result[5], 
                "description": result[6], 
                "year": result[7], 
                "average_rating": result[8],
                "num_pages": result[9],
                "ratings_count": result[10],
                "liked": 0
            } for result in db_output]
    
    return books

def execute_search_query(stmt, count_stmt, engine):
    with engine.connect() as conn:
        total_count = conn.execute(count_stmt).scalar()
        output = conn.execute(stmt)
        results = output.fetchall()
        return results, total_count

def retrieve_book_by_search_input(search_input: str, start: int = 0, end: int = 10, email=None):
    try:
        engine, session = connect_to_db()
        search_input = search_input.lower().strip()

        result = session.query(Book).filter(
            or_(
                Book.title.ilike(f'%{search_input}%'),
                Book.genre.ilike(f'%{search_input}%'),
                Book.author_name.ilike(f'%{search_input}%')
            )
        )

        count_stmt = result.count()
            
        parsed_results = [{
                "book_id": row.book_id,
                "title": row.title,
                "author_name": row.author_name,
                "subtitle": row.subtitle,
                "thumbnail": row.thumbnail,
                "genre": row.genre,
                "description": row.description,
                "year": row.year,
                "average_rating": row.rating,
                "num_pages": row.num_pages,
                "ratings_count": row.ratings_count,
                "liked": 0
            } for row in result.offset(start).limit(end - start)]
        
        if len(parsed_results) > 0:
            if email:
                success, message, liked_books = retrieve_liked_books(email)
                if success:
                    for i, book in enumerate(parsed_results):
                        if book["book_id"] in liked_books:
                            parsed_results[i]["liked"] = 1
                else:
                    return False, message, None, None
            return True, "Books retrieved successfully", parsed_results, count_stmt
        else:
            return False, "Could not retrieve books", None, 0
    except Exception as e:
        return False, str(e), None, 0
    finally:
        session.close()

def get_book_recommendations(email: str):
    try:
        engine, session = connect_to_db()
        stmt = select(Preferences.preference).where(Preferences.email == email)
        with engine.connect() as conn:
            results = conn.execute(stmt)
            genres = list(map(lambda x: x[0], results.fetchall()))
            if len(genres) == 0:
                return False, "User has no preferences", None
            stmt = select(Book.title).where(Book.genre.in_(genres)).limit(5)
            results = conn.execute(stmt)
            recommendations = list(map(lambda x: x[0], results.fetchall()))
            if len(recommendations) == 0:
                return False, "No recommendations found", None
            return True, "Recommendations successfully retrieved", recommendations
    except Exception as e:
        return False, e, None
    finally:
        session.close()


def retrieve_single_book(id):
    try:
        engine, session = connect_to_db()
        stmt = select(Book).where(Book.book_id == id)
        with engine.connect() as conn:
            results = conn.execute(stmt)
            output = results.fetchone()
            if output:
                book = {
                    "book_id": output[0], 
                    "title": output[1], 
                    "genre": output[2], 
                    "description": output[3], 
                    "year": output[4], 
                    "author_id": output[5]
                }
                return True, "Book retreived successfully", book
            else:
                return False, "Error ocurred", None
    except Exception as e:
        print(e)
        return False, e, None
    finally:
        session.close()    

def retrieve_books_from_db(start: int = 1, end: int = 10, order_by=None, email=None):
    try:
        engine, session = connect_to_db()
        if order_by != None:
            stmt = select(Book).offset(start).limit(end - start).order_by(*order_by_map[order_by])
        else:
            stmt = select(Book).offset(start).limit(end - start)
        count_stmt = select(func.count()).select_from(Book)
        
        results, total_count = execute_search_query(stmt, count_stmt, engine)
        parsed_results = parse_output(results)

        if email:
            success, message, liked_books = retrieve_liked_books(email)
            if success:
                print(message)
                for i, book in enumerate(parsed_results):
                    if book["book_id"] in liked_books:
                        parsed_results[i]["liked"] = 1
            else:
                return False, message, None, None
        return True, "Books retrieved successfully", parsed_results, total_count
    except Exception as e:
        print(e)
        return False, str(e), None, 0
    finally:
        session.close()


def delete_book_from_db(book_id):
    try:
        engine, session = connect_to_db()
        with session.begin():
            stmt = delete(Book).where(Book.book_id == book_id)
            result = session.execute(stmt)
            if result.rowcount > 0:
                return True, "Book deleted successfully" 
            else:
                return False, "Book could not be deleted"
    except Exception as e:
        print(e)
        session.rollback()
        return False, e
    finally:
        session.close()

def add_book_to_db(book: Book):
    success, message, author = retrieve_single_author(book.author_id)
    if not success:
        return success, message, None
    
    to_add = Book(
        book_id=book_id,
        title=book.title, 
        subtitle=book.subtitle,
        thumbnail=book.thumbnail,
        author_id=book.author_id,
        author_name=book.author_name,
        genre=book.genre, 
        description=book.description, 
        year=book.year, 
        rating=book.rating,
        num_pages=book.num_pages,
        ratings_count=book.ratings_count   
    )
    
    engine, session = connect_to_db()
    try:
        session.add(to_add)
        session.commit()
        book_id = to_add.book_id
        return True, "Book added Successfully", book_id
    except Exception as e:
        session.rollback()
        return False, e, None
    finally:
        session.close()
        
def edit_book_info(book_id: int, new_book: BookUpdateCurrent):
    success, message, book = retrieve_single_book(book_id)
    if not success:
        return success, message

    if new_book.author_id is not None:
        engine, session = connect_to_db()
        stmt = select(Author.author_id).where(Author.author_id == new_book.author_id)
        with engine.connect() as conn:
            results = conn.execute(stmt)
            output = results.fetchone()
            if not output:
                return False, "New author does not exist"
    
    updated_book_data = {
        "book_id": new_book.book_id if new_book.book_id is not None else book['book_id'],
        "title": new_book.title if new_book.title is not None else book['title'],
        "subtitle": new_book.subtitle if new_book.subtitle is not None else book['subtitle'],
        "thumbnail": new_book.thumbnail if new_book.thumbnail is not None else book['thumbnail'],
        "author_id": new_book.author_id if new_book.author_id is not None else book['author_id'],
        "author_name": new_book.author_name if new_book.author_name is not None else book['author_name'],
        "genre": new_book.genre if new_book.genre is not None else book['genre'],
        "description": new_book.description if new_book.description is not None else book['description'],
        "year": new_book.year if new_book.year is not None else book['year'],
        "rating": new_book.rating if new_book.rating is not None else book['rating'],
        "num_pages": new_book.num_pages if new_book.num_pages is not None else book['num_pages'],
        "ratings_count": new_book.ratings_count if new_book.ratings_count is not None else book['ratings_count'],
    }

    stmt = (
        update(Book)
        .where(Book.book_id == book_id)
        .values(
            book_id=updated_book_data["book_id"],
            title=updated_book_data["title"],
            subtitle=updated_book_data["subtitle"],
            thumbnail=updated_book_data["thumbnail"],
            author_id=updated_book_data["author_id"],
            author_name=updated_book_data["author_name"],
            genre=updated_book_data["genre"],
            description=updated_book_data["description"],
            year=updated_book_data["year"],
            rating=updated_book_data["rating"],
            num_pages=updated_book_data["num_pages"],
            ratings_count=updated_book_data["ratings_count"]
        )
        .execution_options(synchronize_session="fetch")
    )

    try:
        engine, session = connect_to_db()
        with session.begin():
            session.execute(stmt)
            session.commit()
    except Exception as e:
        session.rollback()
        return False, str(e)
    finally:
        session.close()

    return True, "Book information successfully updated"

if __name__ == "__main__":
    pass
    # success, message, output, count = retrieve_book_by_search_input("agatha christie")
    # print(success)
    # print(message)
    # print(output)
    # print(count)
    # success, message = register_liked_book(book_id="0002261987", email="email_0@gmail.com")
    # print("*"*50)
    # print("REGISTER LIKED BOOK")
    # print(message)
    # print("*"*50)
    # success, message = register_liked_book(book_id="0006163831", email="email_0@gmail.com")
    # print("*"*50)
    # print("REGISTER LIKED BOOK")
    # print(message)
    # print("*"*50)
    # success, message, books, count = retrieve_book_by_search_input(search_input="gile", start=0, end=12)
    # print("*"*50)
    # print("SEARCH OUTPUT NO EMAIL")
    # print(message, books)
    # print("*"*50)
    # success, message, books, count = retrieve_books_from_db(start=0, end=12)
    # print("*"*50)
    # print("ALL BOOKS NO EMAIL")
    # print(message, books)
    # print("*"*50)
    # success, message, books, count = retrieve_book_by_search_input(search_input="gile", start=0, end=12, email="email_0@gmail.com")
    # print("*"*50)
    # print("SEARCH OUTPUT WITH EMAIL")
    # print(message, books)
    # print("*"*50)
    # success, message, books, count = retrieve_books_from_db(start=0, end=12, email="email_0@gmail.com")
    # print("*"*50)
    # print("ALL BOOKS WITH EMAIL")
    # print(message, books)
    # print("*"*50)

