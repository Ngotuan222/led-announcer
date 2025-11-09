from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .announcer import Announcement, AnnouncementProcessor
from .config import AppConfig, load_config


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)

LOGGER = logging.getLogger("led-announcer")

CONFIG: AppConfig = load_config()
PROCESSOR = AnnouncementProcessor(CONFIG)


class AnnouncementRequest(BaseModel):
    id: str = Field(..., description="Unique identifier for the person or request")
    fullname: str = Field(..., description="Full name to display and read aloud")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    LOGGER.info("Starting LED announcer service")
    PROCESSOR.start()
    try:
        yield
    finally:
        LOGGER.info("Stopping LED announcer service")
        PROCESSOR.stop()


app = FastAPI(
    title="LED Announcer Service",
    description="Receive announcements and present them on LED display with audio playback",
    version="1.0.0",
    lifespan=lifespan,
)


@app.post("/announce", status_code=202)
async def announce(request: AnnouncementRequest) -> dict[str, str]:
    fullname = request.fullname.strip()
    if not fullname:
        raise HTTPException(status_code=400, detail="fullname must not be empty")

    announcement = Announcement(identifier=request.id, fullname=fullname)
    PROCESSOR.enqueue(announcement)
    LOGGER.info("Announcement accepted for %s", fullname)
    return {"status": "queued", "id": request.id, "fullname": fullname}


@app.get("/healthz")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


