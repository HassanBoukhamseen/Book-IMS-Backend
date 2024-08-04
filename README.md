# README

## Running This Project

To run this project, first cd into the backend directory. Then, within your backend directory, run the following to install all dependancies

```
poetry shell
poetry install
```

Finally, run the following command to turn on the server
```
fastapi dev api.py
```

To open the frontend, simply open `index.html` in a web browser.

## Endpoints Explanation

This document provides brief explanations of the various endpoints available in the application.

### Author Services

- **retrieve_single_author**
  - **Description:** Fetches a single author's details by their ID.
  
- **retrieve_authors_from_db**
  - **Description:** Retrieves a list of all authors from the database.

- **add_author_to_database**
  - **Description:** Adds a new author to the database.

- **edit_author_info**
  - **Description:** Updates information for an existing author in the database.

- **delete_author_from_db**
  - **Description:** Deletes an author from the database by their ID.

### User Services

- **retrieve_single_user**
  - **Description:** Fetches details of a single user by their username.

- **authenticate_user**
  - **Description:** Authenticates a user using their username and password.

- **edit_user_info**
  - **Description:** Updates information for an existing user.

- **register_user**
  - **Description:** Registers a new user in the system.

### Book Services

- **get_book_recommendations**
  - **Description:** Retrieves book recommendations for a user based on their email.

- **retrieve_single_book**
  - **Description:** Fetches details of a single book by its ID.

- **retrieve_books_from_db**
  - **Description:** Retrieves a list of all books from the database.

- **add_book_to_db**
  - **Description:** Adds a new book to the database.

- **delete_book_from_db**
  - **Description:** Deletes a book from the database by its ID.

- **edit_book_info**
  - **Description:** Updates information for an existing book in the database.

### Token Services

- **create_access_token**
  - **Description:** Creates an access token for user authentication.

### Schemas

- **Login**
  - **Description:** Schema for user login information.

- **Author, AuthorUpdateCurrent**
  - **Description:** Schemas for author information and updates.

- **Book, BookUpdateCurrent**
  - **Description:** Schemas for book information and updates.

- **User, UserUpdateCurrent**
  - **Description:** Schemas for user information and updates.

- **UserMessage**
  - **Description:** Schema for user messages.

### Configuration

- **ACCESS_TOKEN_EXPIRE_MINUTES**
  - **Description:** Configuration for the expiration time of access tokens.

### Utilities

- **get_current_user**
  - **Description:** Utility function to get the current authenticated user.

- **get_llm_response**
  - **Description:** Utility function to get a response from a language model.

### FastAPI Endpoints

- **/** (Root Endpoint)
  - **Description:** Returns a simple greeting if the user is authenticated.

- **/books** (GET)
  - **Description:** Retrieves a list of all books if the user is authenticated.

- **/books/{book_id}** (GET)
  - **Description:** Retrieves details of a specific book by its ID if the user is authenticated.

- **/books** (POST) - *Admin Only*
  - **Description:** Adds a new book to the database if the user has admin privileges.

- **/books/{book_id}** (PUT) - *Admin Only*
  - **Description:** Updates information of a specific book by its ID if the user has admin privileges.

- **/books/{book_id}** (DELETE) - *Admin Only*
  - **Description:** Deletes a specific book by its ID if the user has admin privileges.

- **/authors** (GET)
  - **Description:** Retrieves a list of all authors if the user is authenticated.

- **/authors/{author_id}** (GET)
  - **Description:** Retrieves details of a specific author by their ID if the user is authenticated.

- **/authors** (POST) - *Admin Only*
  - **Description:** Adds a new author to the database if the user has admin privileges.

- **/authors/{author_id}** (PUT) - *Admin Only*
  - **Description:** Updates information of a specific author by their ID if the user has admin privileges.

- **/authors/{author_id}** (DELETE) - *Admin Only*
  - **Description:** Deletes a specific author by their ID if the user has admin privileges.

- **/users/register** (POST)
  - **Description:** Registers a new user.

- **/users/login** (POST)
  - **Description:** Authenticates a user and returns an access token if successful.

- **/users/me** (GET)
  - **Description:** Retrieves details of the currently authenticated user.

- **/users/me** (PUT)
  - **Description:** Updates information of the currently authenticated user.

- **/recommendations** (GET)
  - **Description:** Retrieves book recommendations for the authenticated user.

- **/llm_recommendation** (GET)
  - **Description:** Gets a response from a language model based on the user's message.

- **/healthcheck** (GET)
  - **Description:** Performs a health check and returns `True`.
