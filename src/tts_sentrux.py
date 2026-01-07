from __future__ import annotations

import base64
import hashlib
import logging
import subprocess
import tempfile
import threading
from pathlib import Path
from typing import Optional

import requests

from .config import AudioConfig

LOGGER = logging.getLogger(__name__)


class TextToSpeechError(RuntimeError):
    """Raised when the text-to-speech subsystem fails."""


class TextToSpeech:
    API_URL = "https://tts.bio-eco.vn/api/tts"
    VOICES_URL = "https://tts.bio-eco.vn/api/voices"
    AUTH_HEADER = {"Authorization": "Basic c2VudHJ1eDpoa3F0dkAyMDI0"}

    def __init__(self, config: AudioConfig) -> None:
        self._config = config
        self._lock = threading.Lock()
        self._ensure_cache()
        # Default voice if not specified or invalid
        self._voice = "Dung (nữ miền Nam)"

    def _ensure_cache(self) -> None:
        if self._config.cache_dir:
            cache_path = Path(self._config.cache_dir).expanduser()
            cache_path.mkdir(parents=True, exist_ok=True)
            LOGGER.info("Using TTS cache directory: %s", cache_path)

    @property
    def is_playing(self) -> bool:
        """Check if audio is currently being played (or synthesized)."""
        return self._lock.locked()

    def speak(self, text: str) -> None:
        if not text:
            LOGGER.warning("Empty text received for TTS. Skipping playback.")
            return

        with self._lock:
            LOGGER.info("Generating TTS (Sentrux) for: %s", text)
            audio_file = None
            try:
                audio_file = self._synthesize(text)
                self._play(audio_file)
            except Exception as exc:
                LOGGER.error("Error during TTS processing: %s", exc)
                raise
            finally:
                if audio_file and not self._config.cache_dir:
                    audio_file.unlink(missing_ok=True)

    def _synthesize(self, text: str) -> Path:
        # Determine voice from config language if possible, otherwise use default
        # Mapping simple language codes to Sentrux voices could be added here
        # For now, we use the default voice or one specified in config if we extend AudioConfig
        voice = self._voice
        
        # Create a unique hash for the text AND the voice, so changing voice re-generates audio
        text_hash = hashlib.sha256(f"{text}|{voice}".encode("utf-8")).hexdigest()

        if self._config.cache_dir:
            cache_path = Path(self._config.cache_dir).expanduser() / f"{text_hash}.mp3"
            if cache_path.exists():
                LOGGER.debug("Using cached speech for '%s' (hash: %s)", text, text_hash)
                return cache_path
        else:
            cache_path = Path(tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name)

        try:
            payload = {
                "text": text,
                "voice": voice
            }
            headers = {
                "Content-Type": "application/json",
                **self.AUTH_HEADER
            }
            
            LOGGER.debug("Requesting TTS from Sentrux API...")
            response = requests.post(self.API_URL, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if "data" not in data:
                raise TextToSpeechError("Invalid response from Sentrux API: 'data' field missing")
            
            audio_content = base64.b64decode(data["data"])
            
            with open(cache_path, "wb") as f:
                f.write(audio_content)
                
        except requests.RequestException as exc:
            raise TextToSpeechError(f"Sentrux API request failed: {exc}") from exc
        except (ValueError, KeyError) as exc:
            raise TextToSpeechError(f"Failed to parse Sentrux API response: {exc}") from exc

        if not cache_path.exists() or cache_path.stat().st_size == 0:
            raise TextToSpeechError("TTS file generation failed: File is empty or missing")

        LOGGER.debug("Speech synthesized to %s", cache_path)
        return cache_path

    def _play(self, path: Path) -> None:
        if not path.exists():
            LOGGER.error("Audio file not found: %s", path)
            return

        command = list(self._config.playback_command)

        if "__FILE__" in command:
            command = [str(path) if arg == "__FILE__" else arg for arg in command]
        else:
            command.append(str(path))

        LOGGER.info("Playing audio with command: %s", " ".join(command))
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as exc:
            LOGGER.error("Playback failed with stderr: %s", exc.stderr)
            raise TextToSpeechError(f"Failed to play audio: {exc}") from exc
        except FileNotFoundError as exc:
            raise TextToSpeechError(f"Failed to play audio: {exc}") from exc
