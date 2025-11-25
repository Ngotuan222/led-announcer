from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
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

security = HTTPBasic()

try:
    import RPi.GPIO as GPIO
except ImportError:  # pragma: no cover - hardware specific dependency
    GPIO = None  # type: ignore[assignment]
    LOGGER.warning("RPi.GPIO not available. Door control GPIO26 will be disabled.")

DOOR_GPIO_PIN = 5


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    """Simple HTTP Basic authentication for the service."""

    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "hkqt@2024")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


class AnnouncementRequest(BaseModel):
    id: str | None = Field(
        None,
        description="Unique identifier for the person or request (optional when only controlling door)",
    )
    fullname: str | None = Field(
        None,
        description="Full name to display and read aloud (optional when only controlling door)",
    )
    status: str | None = Field(
        None,
        description="Door status: 'open-door' to set GPIO26 HIGH, 'close-door' to set it LOW",
    )


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    LOGGER.info("Starting LED announcer service")
    if GPIO is not None:
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(DOOR_GPIO_PIN, GPIO.OUT, initial=GPIO.LOW)
            LOGGER.info("Door control GPIO initialized on pin %s", DOOR_GPIO_PIN)
        except Exception as exc:  # pragma: no cover - hardware interaction
            LOGGER.exception("Failed to initialize GPIO for door control: %s", exc)

    PROCESSOR.start()
    try:
        yield
    finally:
        LOGGER.info("Stopping LED announcer service")
        PROCESSOR.stop()
        if GPIO is not None:
            try:
                GPIO.cleanup(DOOR_GPIO_PIN)
                LOGGER.info("Cleaned up GPIO pin %s", DOOR_GPIO_PIN)
            except Exception as exc:  # pragma: no cover - hardware interaction
                LOGGER.exception("Failed to clean up GPIO for door control: %s", exc)


def _handle_door_status(status: str | None) -> str | None:
    """Handle door status by toggling GPIO26.

    Returns the effective status applied ("open-door"/"close-door") or None if
    no status was provided.
    """

    if status is None:
        return None

    normalized = status.strip().lower()
    if normalized not in {"open-door", "close-door"}:
        raise HTTPException(
            status_code=400,
            detail="status must be either 'open-door' or 'close-door' when provided",
        )

    if GPIO is None:
        LOGGER.warning(
            "Received door status '%s' but RPi.GPIO is not available; ignoring GPIO control",
            normalized,
        )
        return normalized

    try:
        if normalized == "open-door":
            GPIO.output(DOOR_GPIO_PIN, GPIO.HIGH)
            LOGGER.info("Door status set to OPEN on GPIO %s", DOOR_GPIO_PIN)
        else:  # "close-door"
            GPIO.output(DOOR_GPIO_PIN, GPIO.LOW)
            LOGGER.info("Door status set to CLOSE on GPIO %s", DOOR_GPIO_PIN)
    except Exception as exc:  # pragma: no cover - hardware interaction
        LOGGER.exception("Failed to update door GPIO state: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Failed to update door GPIO state",
        ) from exc

    return normalized


app = FastAPI(
    title="LED Announcer Service",
    description="Receive announcements and present them on LED display with audio playback",
    version="1.0.0",
    lifespan=lifespan,
)


@app.post("/announce", status_code=202)
async def announce(
    request: AnnouncementRequest,
    _: None = Depends(verify_credentials),
) -> dict[str, str]:
    # Handle door status (GPIO26) if provided
    applied_status = _handle_door_status(request.status)

    # Handle announcement (LED + TTS) if fullname is provided
    fullname_raw = request.fullname or ""
    fullname = fullname_raw.strip()

    if not fullname and applied_status is None:
        raise HTTPException(
            status_code=400,
            detail="At least one of 'fullname' or 'status' must be provided",
        )

    response: dict[str, str] = {"status": "ok"}

    if fullname:
        announcement = Announcement(identifier=request.id or "", fullname=fullname)
        PROCESSOR.enqueue(announcement)
        LOGGER.info("Announcement accepted for %s", fullname)
        response.update({"announcement": "queued", "id": request.id or "", "fullname": fullname})

    if applied_status is not None:
        response["door_status"] = applied_status

    return response


@app.get("/healthz")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


