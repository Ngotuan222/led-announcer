from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

import yaml


LOGGER = logging.getLogger(__name__)


@dataclass
class LedDisplayConfig:
    rows: int = 128
    cols: int = 256
    chain_length: int = 1
    parallel: int = 1
    pwm_bits: int = 11
    pwm_lsb_nanoseconds: int = 130
    brightness: int = 70
    gpio_slowdown: int = 4
    hardware_mapping: str = "regular"  # Sử dụng mapping "regular" đã được kiểm tra
    disable_hardware_pulse: bool = True  # Tắt hardware pulse nếu không có root
    font_path: str = "/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf"
    background_color: List[int] = field(default_factory=lambda: [0, 0, 0])
    text_color: List[int] = field(default_factory=lambda: [255, 255, 255])
    hold_seconds: float = 8.0


@dataclass
class AudioConfig:
    language: str = "vi"
    slow: bool = False
    playback_command: List[str] = field(default_factory=lambda: ["mpg123", "-q"])
    cache_dir: str | None = None


@dataclass
class ServiceConfig:
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False


@dataclass
class AppConfig:
    led: LedDisplayConfig = field(default_factory=LedDisplayConfig)
    audio: AudioConfig = field(default_factory=AudioConfig)
    service: ServiceConfig = field(default_factory=ServiceConfig)
    raw: Dict[str, Any] = field(default_factory=dict)


def load_config(path: Path | None = None) -> AppConfig:
    """Load configuration from YAML file, falling back to defaults."""

    if path is None:
        path = Path(__file__).resolve().parent.parent / "config" / "settings.yaml"

    config_data: Dict[str, Any] = {}

    if path.exists():
        LOGGER.info("Loading configuration from %s", path)
        with path.open("r", encoding="utf-8") as handle:
            config_data = yaml.safe_load(handle) or {}
    else:
        LOGGER.warning("Configuration file %s not found. Using defaults.", path)

    led_cfg = LedDisplayConfig(**_get_section(config_data, "led"))
    audio_cfg = AudioConfig(**_get_section(config_data, "audio"))
    service_cfg = ServiceConfig(**_get_section(config_data, "service"))

    return AppConfig(led=led_cfg, audio=audio_cfg, service=service_cfg, raw=config_data)


def _get_section(data: Dict[str, Any], section: str) -> Dict[str, Any]:
    value = data.get(section, {})
    if not isinstance(value, dict):
        LOGGER.warning("Configuration section '%s' is not a mapping. Ignoring.", section)
        return {}
    return value


