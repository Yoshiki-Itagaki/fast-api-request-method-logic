from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status


app = FastAPI()


class Book: 
    id: int
    title: str
    author: str
    description: str
    rating: int    
    published_date: int
    
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "condingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2020
            }
        }
    }
    
    
BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5, 2020),
    Book(2, "Computer Science Pro", "codingwithroby", "A very nice book!", 5, 2020),
    Book(3, "Computer Science Pro", "codingwithroby", "A awesome book!", 5, 2024),
    Book(4, "HP 1", "Author 1", "Book Description!", 2, 2010),
    Book(5, "HP 2", "Author 2", "Book Description!", 3, 2015),
    Book(6, "HP 3", "Author 3", "Book Description!", 1, 2015)
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book        
    raise HTTPException(status_code=404, detail='Item Not Found')

        
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return   


@app.get("/books/published-date/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return            


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))
    

def find_book_id(book: Book):    
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):    
    book_changed = False    
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True            
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item Not Found')    
    
    
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break        
    if not book_deleted:
        raise HTTPException(status_code=404, detail='Item Not Found')
        
    