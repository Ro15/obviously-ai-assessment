from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, Book
from app.schemas import BookCreate, BookUpdate, BookResponse
from app.auth import authenticate_user, create_access_token, get_current_user, get_current_admin, Token, User
from app.events import add_event, router as events_router
from fastapi.security import OAuth2PasswordRequestForm

# Initialize FastAPI application
app = FastAPI( title="Books API",
    description="A FastAPI application for managing books with authentication and real-time updates.",
    version="1.0.0")

# Include SSE router for real-time updates
app.include_router(events_router)    

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Login endpoint
@app.post("/login", response_model=Token, tags=["auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid username or password"
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Create a new book
@app.post("/books/", response_model=BookResponse, tags=["books"])
async def create_book(book: BookCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    add_event(action="created", book_title=db_book.title)
    return db_book

# Get all books with pagination
@app.get("/books/", response_model=list[BookResponse], tags=["books"])
async def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

# Get a specific book by ID
@app.get("/books/{book_id}", response_model=BookResponse, tags=["books"])
async def get_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Update book details
@app.put("/books/{book_id}", response_model=BookResponse, tags=["books"])
async def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    # Add event to queue
    add_event(action="updated", book_title=db_book.title)
    return db_book

# Delete a specific book (admin-only)
@app.delete("/books/{book_id}", tags=["books"])
async def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    # Add event to queue
    add_event(action="deleted", book_title=db_book.title)
    db.delete(db_book)
    db.commit()
    return {"message": f"Book with ID {book_id} has been deleted"}
