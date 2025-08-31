from fastapi import FastAPI,Body 

app = FastAPI()

BOOKS = [
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"title": "Tender Is the Night", "author": "F. Scott Fitzgerald"},
    {"title": "1984", "author": "George Orwell"},
    {"title": "Animal Farm", "author": "George Orwell"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"title": "Pride and Prejudice", "author": "Jane Austen"},
    {"title": "Emma", "author": "Jane Austen"},
    {"title": "The Catcher in the Rye", "author": "J.D.Salinger"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien"},
    {"title": "The Lord of the Rings", "author": "J.R.R. Tolkien"},
]

@app.get("/books")
async def read_books():
    return BOOKS

@app.get("/book/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            return book
    return {"error": "Book not found"}

# Query parameter example
@app.get("/search/")
async def search_books(title: str = None):
    try:
        if title:
            results = [book for book in BOOKS if title.casefold() in book["title"].casefold()]
            return results
        return BOOKS
    except Exception as e:
        return {"error": str(e)}

# Post request 
# POST can have a body that has additional information that GET does not have

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

# PUT request method
# update the information 

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    try:
        for i in range(len(BOOKS)):
            if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
                BOOKS[i] = updated_book
                return "Book updated"
    except Exception as e:
        return f"Error occured while updating:{e}"


# Delete request
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    try:
        for i in range(len(BOOKS)):
            if BOOKS[i].get('title').casefold() == book_title.casefold():
                BOOKS.pop(i)
                return "Book deleted"
        return "Book doesn't exists"
    except Exception as e:
        return f"Error occured while deleting:{e}"
    
# API to fetch all books from a specific author 
@app.get("/books/author_specific")
async def get_author_books(author:str):
    try:
        ans = []
        for i in range(len(BOOKS)):
            if BOOKS[i].get('author').casefold() == author.casefold():
                ans.append(BOOKS[i])
        if len(ans)>0:
            return ans
        return "BOOKS not found"
    except Exception as e:
        return e 

# project/
# │── alembic/               # (if using Alembic for migrations)
# │   └── versions/          
# │
# │── app/
# │   ├── api/               # API routers
# │   │   ├── users.py
# │   │   ├── auth.py
# │   │   ├── items.py
# │   │   └── __init__.py
# │   │
# │   ├── core/              # Core config, security, logging
# │   │   ├── config.py      # Settings via Pydantic (env vars)
# │   │   ├── security.py    # JWT, password hashing
# │   │   ├── logging.py
# │   │   └── __init__.py
# │   │
# │   ├── db/                # Database setup
# │   │   ├── base.py        # Base class for models
# │   │   ├── session.py     # DB session
# │   │   ├── init_db.py     # Populate default data
# │   │   └── __init__.py
# │   │
# │   ├── models/            # SQLAlchemy models
# │   │   ├── user.py
# │   │   ├── item.py
# │   │   └── __init__.py
# │   │
# │   ├── schemas/           # Pydantic schemas
# │   │   ├── user.py
# │   │   ├── item.py
# │   │   └── __init__.py
# │   │
# │   ├── services/          # Business logic
# │   │   ├── user_service.py
# │   │   ├── auth_service.py
# │   │   └── __init__.py
# │   │
# │   ├── utils/             # Helpers/utilities
# │   │   ├── pagination.py
# │   │   └── __init__.py
# │   │
# │   ├── main.py            # Entry point (FastAPI app instance)
# │   └── __init__.py
# │
# │── tests/                 # Unit/integration tests
# │   ├── api/
# │   ├── models/
# │   └── conftest.py
# │
# │── .env                   # Environment variables
# │── .env.example           # Example env file
# │── requirements.txt       # Dependencies (or pyproject.toml if using poetry)
# │── Dockerfile             # Docker support
# │── docker-compose.yml     # Optional (DB, cache, etc.)
# │── alembic.ini            # Alembic config
# │── README.md
