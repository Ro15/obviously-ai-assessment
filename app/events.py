from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal, Book
from datetime import datetime
import asyncio

router = APIRouter()

# A global queue to store book events
book_event_queue = []

def get_db():
    """
    Dependency to get the database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_event(action: str, book_title: str):
    """
    Adds a book event to the queue for SSE.
    Keeps only the last 5 events.
    """
    event = {
        "action": action,
        "book_title": book_title,
        "last_updated": datetime.utcnow().isoformat(),
    }
    book_event_queue.append(event)
    # Ensure the queue only keeps the last 5 updates
    if len(book_event_queue) > 5:
        book_event_queue.pop(0)

@router.get("/books/updates", tags=["books"])
async def book_updates():
    """
    Server-Sent Events (SSE) endpoint for the last 5 book updates.
    Streams events with action, book title, and last updated time.
    """

    async def event_stream():
        """
        Stream the last 5 book events.
        """
        if not book_event_queue:
            # If no updates exist, send a placeholder message
            yield f"data: {{\"action\": \"no_updates\", \"message\": \"No updates available\", \"last_checked\": \"{datetime.utcnow().isoformat()}\"}}\n\n"
        else:
            # Send the last 5 events
            for event in book_event_queue:
                yield f"data: {event}\n\n"
        
        # Close the stream
        yield "event: close\ndata: Stream ended\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
