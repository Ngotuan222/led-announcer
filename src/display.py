from __future__ import annotations

import logging
import threading
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .config import LedDisplayConfig


LOGGER = logging.getLogger(__name__)


try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
except ImportError:  # pragma: no cover - hardware specific dependency
    RGBMatrix = None  # type: ignore[assignment]
    RGBMatrixOptions = object  # type: ignore[assignment]
    graphics = None  # type: ignore[assignment]


class LedDisplayUnavailable(RuntimeError):
    """Raised when LED display hardware is not accessible."""


@dataclass
class LedDisplay:
    config: LedDisplayConfig
    _matrix: Optional[RGBMatrix] = None
    _lock: threading.Lock = threading.Lock()
    _previous_text: str = ""  # Lưu text cũ cho dòng trên

    def __post_init__(self) -> None:
        if RGBMatrix is None:
            raise LedDisplayUnavailable(
                "rgbmatrix bindings could not be imported. "
                "Install rpi-rgb-led-matrix and run on compatible hardware."
            )

        options = self._build_options()
        self._matrix = RGBMatrix(options=options)
        self._font = self._load_font(self.config.font_path)
        color_vals = self.config.text_color
        self._text_color = graphics.Color(*color_vals)
        bg_vals = self.config.background_color
        self._bg_color = graphics.Color(*bg_vals)
        LOGGER.info(
            "LED display initialized: %sx%s, chain=%s, parallel=%s",
            self.config.cols,
            self.config.rows,
            self.config.chain_length,
            self.config.parallel,
        )

    def _build_options(self) -> RGBMatrixOptions:
        options = RGBMatrixOptions()
        options.rows = self.config.rows
        options.cols = self.config.cols
        options.chain_length = self.config.chain_length
        options.parallel = self.config.parallel
        options.pwm_bits = self.config.pwm_bits
        options.pwm_lsb_nanoseconds = self.config.pwm_lsb_nanoseconds
        options.brightness = self.config.brightness
        options.gpio_slowdown = self.config.gpio_slowdown
        options.hardware_mapping = self.config.hardware_mapping
        options.drop_privileges = False
        # Tắt hardware pulse nếu không có root (tránh lỗi permission)
        if self.config.disable_hardware_pulse:
            options.disable_hardware_pulsing = True
        return options

    @staticmethod
    def _load_font(font_path: str):
        font = graphics.Font()
        resolved = Path(font_path).expanduser().resolve()
        if not resolved.exists():
            raise FileNotFoundError(f"Font file not found: {resolved}")
        font.LoadFont(str(resolved))
        return font

    @staticmethod
    def _remove_vietnamese_diacritics(text: str) -> str:
        """
        Chuyển đổi text tiếng Việt có dấu sang không dấu.
        Các font BDF mặc định không hỗ trợ Unicode/dấu tiếng Việt.
        """
        # Normalize Unicode (NFD - decomposed form)
        text = unicodedata.normalize('NFD', text)
        # Loại bỏ các ký tự dấu (combining characters)
        text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
        # Chuyển đổi một số ký tự đặc biệt
        text = text.replace('đ', 'd').replace('Đ', 'D')
        return text

    def show_text(self, text: str) -> None:
        if self._matrix is None:
            raise LedDisplayUnavailable("LED matrix not initialized")

        with self._lock:
            # Chuyển đổi text tiếng Việt có dấu sang không dấu
            # Vì các font BDF mặc định không hỗ trợ Unicode/dấu
            display_text = self._remove_vietnamese_diacritics(text)
            
            LOGGER.debug("Rendering text on LED display: '%s' -> '%s'", text, display_text)
            canvas = self._matrix.CreateFrameCanvas()
            canvas.Clear()

            # Tính kích thước màn hình thực tế
            # Với chain_length và parallel, màn hình thực tế lớn hơn
            total_rows = self.config.rows * self.config.parallel
            total_cols = self.config.cols * self.config.chain_length
            
            # Tính baseline: giữa màn hình theo chiều dọc
            # Trong graphics.DrawText, tham số y là baseline (điểm dưới cùng của text)
            # Để text nằm giữa: baseline = giữa màn hình + một nửa chiều cao font
            font_height = self._font.height
            # Với màn hình 32x64 và font 6x10:
            # total_rows = 32, font_height = 10
            # baseline = 16 + 5 = 21 (text sẽ nằm từ y=11 đến y=21, giữa là y=16)
            baseline = total_rows // 2 + font_height // 2
            
            # Tính chiều dài text để căn giữa (dựa trên tổng chiều ngang)
            # Sử dụng canvas tạm để đo chiều dài text
            temp_canvas = self._matrix.CreateFrameCanvas()
            text_length = graphics.DrawText(
                temp_canvas,
                self._font,
                0,
                baseline,
                self._text_color,
                display_text,
            )

            # Căn giữa text theo chiều ngang
            start_x = max((total_cols - text_length) // 2, 0)
            
            # Đảm bảo text không bị cắt (nếu text quá dài, bắt đầu từ 0)
            if start_x + text_length > total_cols:
                start_x = 0
                LOGGER.warning(
                    "Text too long (%d pixels) for screen width (%d), starting at 0",
                    text_length, total_cols
                )
            
            # Vẽ text lên canvas
            canvas.Clear()
            graphics.DrawText(
                canvas,
                self._font,
                start_x,
                baseline,
                self._text_color,
                display_text,
            )

            self._matrix.SwapOnVSync(canvas)
            LOGGER.debug(
                "Text rendered: '%s' -> '%s' at (%d, %d), length=%d, total_size=%dx%d",
                text, display_text, start_x, baseline, text_length, total_cols, total_rows
            )
            LOGGER.debug("Swap complete. Holding frame for %.2f seconds", self.config.hold_seconds)
            if self.config.hold_seconds > 0:
                time.sleep(self.config.hold_seconds)

    def show_scrolling_text(self, text: str, scroll_speed: float = 0.1) -> None:
        """
        Hiển thị text chạy ngang từ phải sang trái trên 2 hàng:
        - Dòng trên: text cũ (scrolling)
        - Dòng dưới: text mới (scrolling)
        """
        if self._matrix is None:
            raise LedDisplayUnavailable("LED matrix not initialized")

        with self._lock:
            # Chuyển đổi text tiếng Việt có dấu sang không dấu
            display_text = self._remove_vietnamese_diacritics(text)
            previous_display_text = self._remove_vietnamese_diacritics(self._previous_text)
            
            LOGGER.debug("Rendering 2-line scrolling text: previous='%s' -> '%s', new='%s' -> '%s'", 
                        self._previous_text, previous_display_text, text, display_text)
            canvas = self._matrix.CreateFrameCanvas()

            # Tính kích thước màn hình thực tế
            total_rows = self.config.rows * self.config.parallel
            total_cols = self.config.cols * self.config.chain_length
            
            # Tính vị trí cho 2 dòng
            font_height = self._font.height
            
            # Dòng trên (text cũ): ở vị trí 1/3 từ trên xuống - dịch lên trên 3 pixel (2+1)
            top_baseline = total_rows // 3 + font_height // 2 - 3
            
            # Dòng dưới (text mới): ở vị trí 2/3 từ trên xuống - dịch lên trên 1 pixel
            bottom_baseline = (total_rows * 2) // 3 + font_height // 2 - 1
            
            # Tính chiều dài text mới và text cũ
            temp_canvas = self._matrix.CreateFrameCanvas()
            new_text_length = graphics.DrawText(
                temp_canvas,
                self._font,
                0,
                bottom_baseline,
                self._text_color,
                display_text,
            )
            
            # Tính chiều dài text cũ
            prev_text_length = 0
            if previous_display_text:
                prev_text_length = graphics.DrawText(
                    temp_canvas,
                    self._font,
                    0,
                    top_baseline,
                    self._text_color,
                    previous_display_text,
                )

            # Xác định text dài nhất để làm thời gian chạy
            max_length = max(new_text_length, prev_text_length)
            
            # Nếu cả 2 text đều ngắn hơn màn hình, hiển thị tĩnh
            if max_length <= total_cols:
                canvas.Clear()
                
                # Dòng trên: text cũ (căn giữa)
                if previous_display_text:
                    prev_start_x = max((total_cols - prev_text_length) // 2, 0)
                    graphics.DrawText(
                        canvas,
                        self._font,
                        prev_start_x,
                        top_baseline,
                        self._text_color,
                        previous_display_text,
                    )
                
                # Dòng dưới: text mới (căn giữa)
                new_start_x = (total_cols - new_text_length) // 2
                graphics.DrawText(
                    canvas,
                    self._font,
                    new_start_x,
                    bottom_baseline,
                    self._text_color,
                    display_text,
                )
                
                self._matrix.SwapOnVSync(canvas)
                if self.config.hold_seconds > 0:
                    time.sleep(self.config.hold_seconds)
            else:
                # Một trong hai text dài hơn màn hình: chạy cả 2 từ phải sang trái
                # Bắt đầu từ bên phải màn hình
                start_x = total_cols
                # Kết thúc khi text dài nhất chạy qua bên trái màn hình
                end_x = -max_length
                
                for x in range(start_x, end_x, -1):
                    canvas.Clear()
                    
                    # Dòng trên: text cũ (scrolling)
                    if previous_display_text:
                        # Nếu text cũ ngắn, căn giữa khi chạy
                        if prev_text_length <= total_cols:
                            # Text ngắn: căn giữa trong khi chạy theo text dài
                            prev_x = x + (max_length - prev_text_length) // 2
                        else:
                            # Text dài: chạy bình thường
                            prev_x = x
                        
                        graphics.DrawText(
                            canvas,
                            self._font,
                            prev_x,
                            top_baseline,
                            self._text_color,
                            previous_display_text,
                        )
                    
                    # Dòng dưới: text mới (scrolling)
                    # Nếu text mới ngắn, căn giữa khi chạy
                    if new_text_length <= total_cols:
                        # Text ngắn: căn giữa trong khi chạy theo text dài
                        new_x = x + (max_length - new_text_length) // 2
                    else:
                        # Text dài: chạy bình thường
                        new_x = x
                    
                    graphics.DrawText(
                        canvas,
                        self._font,
                        new_x,
                        bottom_baseline,
                        self._text_color,
                        display_text,
                    )
                    
                    self._matrix.SwapOnVSync(canvas)
                    time.sleep(scroll_speed)

            # Lưu text hiện tại làm text cũ cho lần tiếp theo
            self._previous_text = text

    def clear(self) -> None:
        if self._matrix is None:
            return
        with self._lock:
            canvas = self._matrix.CreateFrameCanvas()
            canvas.Clear()
            self._matrix.SwapOnVSync(canvas)
            self._previous_text = ""  # Xóa text cũ
            LOGGER.debug("LED display cleared")


