# Library Management System

A web-based library management system where users can sign up, log in, and manage their own authors and books. Each user has a separate set of records, with data isolation enforced through user ownership and database relationships.

**Course:** Database Systems Lab  
**Faculty:** Alexandria National University

---

## 1. Team

| Name | ID | What this person did |
|---|---|---|
| Mohamed Ali Mohamed | 2304105 | Database design, MySQL, Flask backend, authentication, data isolation, CRUD operations, frontend integration, and testing |
| Waleed Mohamed Ibrahim | 2304097 | [Frontend design, CSS, JavaScript, testing, or other contributions] |
## 2. Technology

- **Back end:** Python with Flask
- **Front end:** HTML5, CSS3, and JavaScript
- **Database:** MySQL (`library_db`), using plain SQL without an ORM
- **Database connection:** `mysql-connector-python`
- **Authentication:** Flask sessions and Werkzeug password hashing
- **Interface:** Responsive design with Arabic (RTL) support
- **Security:** User-specific data access and parameterized SQL queries

## 3. How to Run It

1. Install Python and MySQL Server. MySQL Workbench can be used to manage the database.
2. Download or clone this project from GitHub.
3. Open MySQL Workbench and connect to your local MySQL Server.
4. Create the `library_db` database and its tables using the project's SQL script, if available. Otherwise, create the tables according to the Database Design section.
5. Configure the database connection in the Flask application using your local MySQL host, username, password, and database name.
6. Open a terminal in the project folder and install the required packages:

```bash
pip install Flask mysql-connector-python Werkzeug
```

7. Start the application:

```bash
python app.py
```

8. Open the website in your browser:

```text
http://127.0.0.1:5000
```

**Note:** The Flask server must remain running while using the application. Database connection settings and installation requirements should match the actual project files.

---

## 4. Database Design

The application uses a MySQL database named `library_db` containing three main tables: `users`, `AUTHOR`, and `BOOK`.

### Users

Stores registered user accounts.

| Column | Description |
|---|---|
| `id` | Primary key, auto-increment |
| `name` | User's name |
| `email` | User's email, unique |
| `password` | Hashed password |

### AUTHOR

Stores author records belonging to individual users.

| Column | Description |
|---|---|
| `author_id` | Primary key, auto-increment |
| `name` | Author's name |
| `country` | Author's country |
| `user_id` | Foreign key referencing `users(id)`, identifying the owner |

### BOOK

Stores book records and their associated authors.

| Column | Description |
|---|---|
| `book_id` | Primary key, auto-increment |
| `title` | Book title |
| `price` | Book price |
| `author_id` | Foreign key referencing `AUTHOR(author_id)` |
| `user_id` | Foreign key referencing `users(id)`, identifying the owner |

### Relationships

- **Users and Authors:** One user can have multiple authors. Each author belongs to a user through `AUTHOR.user_id`.
- **Users and Books:** One user can have multiple books. Each book belongs to a user through `BOOK.user_id`.
- **Authors and Books:** One author can have multiple books. Each book references its author through `BOOK.author_id`.

### Data Isolation

Each user's author and book records must remain separate from those of other users.

The `user_id` column identifies the owner of each record. The Flask application uses the authenticated user's identity from the session to restrict database operations to records that belong to that user.

For example, when a user opens the dashboard, the application should retrieve only that user's authors and books. Edit and delete operations must also verify ownership before changing or removing a record.

This prevents one user from accessing or modifying another user's data by changing a record ID in a URL or form.

**Important:** Foreign keys maintain referential integrity, but they do not automatically enforce user ownership across related records. The application must also verify that a book's author belongs to the same user. Database constraints can provide additional protection where appropriate.

### Referential Integrity

The `BOOK.author_id` foreign key maintains the relationship between books and authors. The existing `ON DELETE CASCADE` behavior means that deleting an author automatically deletes books referencing that author.

This behavior should be considered carefully because deleting an author can remove multiple associated books.

---

## 5. Features

- **R1 — Registration:** Users can create accounts with their name, email, and password. Email addresses must be unique.
- **R2 — Login and Logout:** Users can log in and log out. Flask sessions maintain authentication state.
- **R3 — Protected Dashboard:** Only authenticated users can access the dashboard.
- **R4 — View Authors:** Display the authenticated user's author records.
- **R5 — Add Authors:** Create new author records associated with the logged-in user.
- **R6 — Edit Authors:** Update an author's information after verifying ownership.
- **R7 — Delete Authors:** Delete an author's record using a POST request and enforce ownership checks. Associated books are deleted according to the foreign key's cascade rule.
- **R8 — View Books:** Display books belonging to the authenticated user.
- **R9 — Add Books:** Add books and select an author from the available author list belonging to the same user.
- **R10 — Edit Books:** Update a book's title, price, or author after verifying ownership and the selected author's ownership.
- **R11 — Delete Books:** Delete individual book records after verifying ownership.
- **R12 — Database Integration:** Connect Flask to MySQL using `mysql-connector-python` and plain SQL queries.
- **R13 — Password Security:** Store password hashes using Werkzeug instead of storing plain-text passwords.
- **R14 — Data Isolation:** Keep each user's author and book records separate from those of other users.
- **R15 — User Interface:** Provide consistent styling, responsive layouts, Arabic right-to-left support, and JavaScript delete-confirmation dialogs.

---

## 6. Screenshots

Place actual screenshots of the application in the `screenshots/` directory.

### Registration Page

![Registration page](screenshots/register.png)

### Login Page

![Login page](screenshots/login.png)

### Dashboard

![Library dashboard](screenshots/dashboard.png)

### Add or Edit Author

![Author form](screenshots/author_form.png)

### Add or Edit Book

![Book form](screenshots/book_form.png)

### Delete Confirmation

![Delete confirmation](screenshots/delete_confirmation.png)

*Replace or remove any screenshot references that do not match the actual files in the repository.*

---

## 7. Database Systems Questions and Answers

**(a) What is the purpose of a primary key in the `AUTHOR` and `BOOK` tables?**

A primary key uniquely identifies each record in a table. For example, `author_id` identifies an author, while `book_id` identifies a book. This allows the application to reference and update records reliably.

**(b) Why does the `BOOK` table contain a foreign key referencing `AUTHOR`?**

The `author_id` foreign key establishes the relationship between a book and its author. It helps maintain referential integrity by ensuring that the referenced author exists.

**(c) What is the purpose of adding `user_id` to the `AUTHOR` and `BOOK` tables?**

The `user_id` column identifies the user who owns each author or book record. It allows the application to retrieve and manage records according to their owner, rather than displaying all users' records together.

**(d) How does data isolation work in this application?**

After login, Flask maintains the authenticated user's identity in the session. Database queries use that identity to restrict access to the user's records. Edit and delete operations must also verify ownership, so knowing another user's record ID is not enough to modify their data.

**(e) What could happen if an UPDATE or DELETE query checks only the record ID but not `user_id`?**

If the application does not verify ownership, a logged-in user could potentially modify or delete another user's record by supplying its ID. Adding an ownership condition such as `AND user_id = %s`, using the authenticated user's ID, helps prevent this problem. The application must also validate ownership for related records.

**(f) What happens if a book references an `author_id` that does not exist?**

MySQL rejects the insertion because it violates the foreign key constraint. This commonly produces error code `1452`.

**(g) What does `ON DELETE CASCADE` do?**

When an author is deleted, MySQL automatically deletes books referencing that author through the configured foreign key. This prevents orphaned book records, but it also means that multiple books may be deleted together.

**(h) Why are passwords stored as hashes instead of plain text?**

Password hashing reduces the risk of exposing users' actual passwords if the database is compromised. Werkzeug provides password-hashing and verification functions. During login, the submitted password is checked against the stored hash.

**(i) Why does the application use Flask sessions?**

Sessions allow Flask to maintain authentication state between requests. The application can identify the logged-in user and use that identity to protect routes and restrict database operations.

**(j) Why should SQL queries use parameterized statements?**

Parameterized queries separate SQL commands from user-provided values. This helps prevent SQL injection by ensuring that user input is treated as data rather than executable SQL.

**(k) Why are delete operations submitted using POST forms?**

POST requests are appropriate for state-changing operations such as deletion. The server must still validate the request, enforce ownership, and apply appropriate security protections.

---

## 8. Conclusion

The Library Management System demonstrates the integration of a relational database with a Flask web application using MySQL. It applies primary keys, foreign keys, referential integrity, CRUD operations, cascading deletes, authentication, and user-specific data isolation.

The project also demonstrates how a backend can connect a frontend to a relational database while ensuring that users manage their own records through a local web application.
