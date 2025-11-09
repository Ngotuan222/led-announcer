from __future__ import annotations

import logging
import queue
import threading
import time
from dataclasses import dataclass
from typing import Callable, Optional

from .config import AppConfig
from .display import LedDisplay, LedDisplayUnavailable
from .tts import TextToSpeech, TextToSpeechError


LOGGER = logging.getLogger(__name__)


@dataclass
class Announcement:
    identifier: str
    fullname: str


class AnnouncementProcessor:
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._queue: "queue.Queue[Announcement]" = queue.Queue()
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

        self._display = self._initialize_display()
        self._tts = TextToSpeech(config.audio)

    def _initialize_display(self) -> Optional[LedDisplay]:
        try:
            return LedDisplay(self._config.led)
        except (LedDisplayUnavailable, FileNotFoundError) as exc:
            LOGGER.error("LED display unavailable: %s", exc)
            LOGGER.warning("Continuing without LED output. Only audio will play.")
            return None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return

        self._thread = threading.Thread(target=self._run, name="announcement-worker", daemon=True)
        self._thread.start()
        LOGGER.info("Announcement processor started")

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._queue.put(None)  # type: ignore[arg-type]
            self._thread.join(timeout=5)
        if self._display:
            self._display.clear()
        LOGGER.info("Announcement processor stopped")

    def enqueue(self, announcement: Announcement) -> None:
        LOGGER.debug("Queueing announcement: %s", announcement)
        self._queue.put(announcement)

    def _run(self) -> None:
        while not self._stop_event.is_set():
            try:
                item = self._queue.get(timeout=0.5)
            except queue.Empty:
                continue

            if item is None:  # type: ignore[unreachable]
                LOGGER.debug("Received sentinel, stopping worker")
                break

            self._handle(item)
            self._queue.task_done()

    def _handle(self, announcement: Announcement) -> None:
        LOGGER.info("Handling announcement for %s (%s)", announcement.fullname, announcement.identifier)

        # Tạo và chạy thread riêng cho LED để chạy nền
        led_thread = None
        if self._display:
            led_thread = threading.Thread(
                target=self._display_worker,
                args=(announcement.fullname,),
                name="led-worker",
                daemon=True
            )
            led_thread.start()

        # TTS chạy chính và đợi xong
        try:
            self._tts.speak(announcement.fullname)
        except TextToSpeechError as exc:
            LOGGER.exception("Failed to play TTS audio: %s", exc)

        # Không đợi LED thread hoàn thành - LED tiếp tục chạy ở nền
        LOGGER.debug("TTS completed, LED continues in background")

        time.sleep(0.1)

    def _display_worker(self, fullname: str) -> None:
        """Worker thread cho LED display"""
        try:
            self._display.show_scrolling_text(fullname, scroll_speed=0.025)
        except Exception as exc:  # pragma: no cover - hardware interaction
            LOGGER.exception("Failed to update LED display: %s", exc)
