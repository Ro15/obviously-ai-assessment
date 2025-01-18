import time
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
from datetime import datetime

router = APIRouter()

@router.get("/books/updates", tags=["books"])
async def book_updates():
    async def event_stream():
        while True:
            await asyncio.sleep(2)
            yield f"data: A book update at {datetime.utcnow()}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
