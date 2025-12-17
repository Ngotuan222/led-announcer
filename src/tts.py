from __future__ import annotations

import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import List

from gtts import gTTS

from .config import AudioConfig


LOGGER = logging.getLogger(__name__)


class TextToSpeechError(RuntimeError):
    """Raised when the text-to-speech subsystem fails."""


class TextToSpeech:
    def __init__(self, config: AudioConfig) -> None:
        self._config = config
        self._ensure_cache()

    def _ensure_cache(self) -> None:
        if self._config.cache_dir:
            cache_path = Path(self._config.cache_dir).expanduser()
            cache_path.mkdir(parents=True, exist_ok=True)
            LOGGER.info("Using TTS cache directory: %s", cache_path)

    def speak(self, text: str) -> None:
        if not text:
            LOGGER.warning("Empty text received for TTS. Skipping playback.")
            return

        LOGGER.info("Generating TTS for: %s", text)
        audio_file = self._synthesize(text)

        try:
            self._play(audio_file)
        finally:
            if not self._config.cache_dir:
                audio_file.unlink(missing_ok=True)

    def _synthesize(self, text: str) -> Path:
        if self._config.cache_dir:
            sanitized = text.strip().replace(" ", "_")[:64]
            cache_path = Path(self._config.cache_dir).expanduser() / f"{sanitized}.mp3"
            if cache_path.exists():
                LOGGER.debug("Using cached speech for '%s'", text)
                return cache_path
        else:
            cache_path = Path(tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name)

        tts = gTTS(text=text, lang=self._config.language, slow=self._config.slow)
        tts.save(str(cache_path))
        LOGGER.debug("Speech synthesized to %s", cache_path)
        return cache_path

    def _play(self, path: Path) -> None:
        command = list(self._config.playback_command)

        # Hỗ trợ placeholder đặc biệt "__FILE__" trong playback_command để
        # chỉ định chính xác vị trí chèn đường dẫn file âm thanh.
        # Ví dụ trong settings.yaml:
        #   playback_command: ["/usr/bin/play", "-q", "__FILE__", "tempo", "1.5"]
        # sẽ trở thành:
        #   /usr/bin/play -q /path/to/file.mp3 tempo 1.5
        if "__FILE__" in command:
            command = [str(path) if arg == "__FILE__" else arg for arg in command]
        else:
            command.append(str(path))

        LOGGER.info("Playing audio with command: %s", " ".join(command))
        try:
            subprocess.run(command, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError) as exc:
            raise TextToSpeechError(f"Failed to play audio: {exc}") from exc
