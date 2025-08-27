from fastapi import FastAPI, Body,Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id:int 
    title:str
    author:str
    rating:int 
    published_date:int 
    def __init__(self,id,title,author,rating,published_date):
        self.id = id 
        self.title = title
        self.author = author
        self.rating = rating
        self.published_date =  published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create',default=None)
    title: str = Field(min_length=5)
    author: str = Field(min_length=5, max_length=50)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1900, lt=2025)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "rating": 5,
                "published_date": 1925
            }
        }
    }

BOOKS = [
    Book(1, "The Great Gatsby", "F. Scott Fitzgerald", 5, 1925),
    Book(2, "Tender Is the Night", "F. Scott Fitzgerald", 4, 1934),
    Book(3, "1984", "George Orwell", 5, 1949),
    Book(4, "Animal Farm", "George Orwell", 4, 1945),
    Book(5, "To Kill a Mockingbird", "Harper Lee", 5, 1960),
    Book(6, "Pride and Prejudice", "Jane Austen", 5, 1813),
    Book(7, "Emma", "Jane Austen", 4, 1815),
    Book(8, "The Catcher in the Rye", "J.D.Salinger", 4, 1951),
    Book(9, "The Hobbit", "J.R.R. Tolkien", 5, 1937),
    Book(10, "The Lord of the Rings", "J.R.R. Tolkien", 5, 1954),
]

@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS 

@app.get("/books/{book_id}")
async def read_book(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book 
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/books/")
async def read_book_by_rating(book_rating:int = Query(gt=0, lt=6)):
    bl = []
    for book in BOOKS:
        if book.rating == book_rating:
            bl.append(book)
    return bl


@app.get("/books/search/{p_date}")
async def search_by_date(p_date:int):
    bl = []
    for book in BOOKS:
        if book.published_date and book.published_date == p_date:
            bl.append(book)
    return bl

@app.post("/create-books",status_code=status.HTTP_201_CREATED)
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.dict())
    # this is to simulate a database append operation and new_book is added to the list of BOOKS
    BOOKS.append(find_book_id(new_book))
    return BOOKS    

def find_book_id(book: Book):
    if len(BOOKS)>0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book

@app.put("/books/updatebooks")
async def update_book(book_update:BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_update.id:
            BOOKS[i].title = book_update.title
            BOOKS[i].author = book_update.author
            BOOKS[i].rating = book_update.rating
            return BOOKS[i]
    raise HTTPException(status_code=404, detail="Book not found, cannot update")

# delete a book
@app.delete("/books/deletebook/{book_id}")
async def delete_book(book_id:int): 
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return HTTPException(status_code=200, detail="Book deleted successfully")
    raise HTTPException(status_code=404, detail="Book not found, cannot delete")

