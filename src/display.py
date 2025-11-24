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
    _current_animation_id: int = 0  # Nhận diện animation hiện tại của show_scrolling_text

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
            options.scan_mode = self.config.scan_mode
        # Áp dụng cấu hình multiplexing nếu có
        options.multiplexing = self.config.multiplexing
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

    def _wrap_text_to_lines(self, text: str, max_width: int) -> list[str]:
        if self._matrix is None:
            raise LedDisplayUnavailable("LED matrix not initialized")

        words = text.split()
        if not words:
            return [""]

        lines: list[str] = []
        current_line = ""
        temp_canvas = self._matrix.CreateFrameCanvas()

        for word in words:
            tentative = (current_line + " " + word).strip()
            width = graphics.DrawText(
                temp_canvas,
                self._font,
                0,
                self._font.height,
                self._text_color,
                tentative,
            )

            if width <= max_width or not current_line:
                current_line = tentative
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def show_text(self, text: str) -> None:
        if self._matrix is None:
            raise LedDisplayUnavailable("LED matrix not initialized")

        with self._lock:
            # Chuyển đổi text tiếng Việt có dấu sang không dấu
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
            # Dời toàn bộ text lên trên 3 pixel
            # Dịch thêm 1 pixel nữa để toàn bộ nội dung nằm cao hơn
            baseline = total_rows // 2 + font_height // 2 - 3
            
            
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
        Hiển thị text chạy dọc từ dưới lên, căn giữa theo chiều ngang.

        - Nếu text (sau khi wrap) thấp hơn hoặc bằng chiều cao màn hình:
          cuộn một lần đến vị trí giữa rồi dừng và giữ frame.
        - Nếu text cao hơn màn hình:
          cuộn từ dưới lên, hết một vòng thì lặp lại cho đến khi có API mới.
        """
        if self._matrix is None:
            raise LedDisplayUnavailable("LED matrix not initialized")

        # Mỗi lần gọi gán một animation_id mới, để vòng cuộn cũ biết khi nào cần dừng
        self._current_animation_id += 1
        animation_id = self._current_animation_id

        # Chuyển đổi text tiếng Việt có dấu sang không dấu
        display_text = self._remove_vietnamese_diacritics(text)

        LOGGER.debug(
            "Rendering vertical scrolling text (full): '%s' -> '%s' (animation_id=%d)",
            text,
            display_text,
            animation_id,
        )

        # Chuẩn bị canvas riêng cho animation này
        canvas = self._matrix.CreateFrameCanvas()

        # Tính kích thước màn hình thực tế
        total_rows = self.config.rows * self.config.parallel
        total_cols = self.config.cols * self.config.chain_length

        # Chiều cao font và khoảng cách giữa các dòng
        font_height = self._font.height
        line_spacing = max(2, font_height // 4)

        # Wrap toàn bộ text thành nhiều dòng (không giới hạn) theo chiều rộng màn hình
        lines = self._wrap_text_to_lines(display_text, total_cols)
        num_lines = len(lines)

        # Tính tổng chiều cao khối text
        text_block_height = num_lines * font_height + max(0, num_lines - 1) * line_spacing

        # Tâm màn hình theo chiều dọc (dịch toàn bộ nội dung lên trên 1 pixel)
        center_row = total_rows // 2 - 1

        # Căn khối text quanh tâm màn hình theo chiều dọc
        top_center = center_row - text_block_height // 2

        # Chuẩn bị baseline và vị trí X cho từng dòng
        baselines: list[int] = []
        start_x_list: list[int] = []

        temp_canvas = self._matrix.CreateFrameCanvas()
        for i, line in enumerate(lines):
            line_top = top_center + i * (font_height + line_spacing)
            baseline = line_top + font_height
            baselines.append(baseline)

            length = graphics.DrawText(
                temp_canvas,
                self._font,
                0,
                baseline,
                self._text_color,
                line,
            )
            start_x = max((total_cols - length) // 2, 0)
            start_x_list.append(start_x)

        # Tính toán phạm vi cuộn:
        # - Nếu toàn bộ text nằm vừa màn hình, chỉ cuộn đến đúng tâm rồi dừng.
        # - Nếu text cao hơn màn hình, lặp lại hiệu ứng cuộn từ dưới lên vô hạn
        #   (cho tới khi có API mới gọi hàm này với text khác).
        fits_on_screen = text_block_height <= total_rows

        if fits_on_screen:
            # Trường hợp text thấp, chỉ cần cuộn một lần rồi dừng ở giữa
            start_offset = total_rows
            end_offset = 0

            for offset in range(start_offset, end_offset - 1, -1):
                # Nếu đã có animation mới, dừng ngay
                if animation_id != self._current_animation_id:
                    LOGGER.debug("Animation %d cancelled before finishing short scroll", animation_id)
                    return

                with self._lock:
                    canvas.Clear()
                    for i, line in enumerate(lines):
                        y = baselines[i] + offset
                        # Chỉ vẽ nếu phần baseline còn nằm trong vùng hiển thị mở rộng
                        if y < -font_height or y > total_rows + font_height:
                            continue
                        graphics.DrawText(
                            canvas,
                            self._font,
                            start_x_list[i],
                            y,
                            self._text_color,
                            line,
                        )
                    self._matrix.SwapOnVSync(canvas)
                time.sleep(scroll_speed)

            # Với text ngắn (nằm gọn trong màn hình), giữ nguyên frame ở giữa theo cấu hình
            hold_seconds = getattr(self.config, "short_text_hold_seconds", 10.0)
            if animation_id == self._current_animation_id and hold_seconds > 0:
                LOGGER.debug(
                    "Holding centered scrolling frame for %.2f seconds (animation_id=%d)",
                    hold_seconds,
                    animation_id,
                )
                # Chia nhỏ thời gian chờ để nếu có animation mới thì dừng ngay
                step = 0.1
                steps = int(hold_seconds / step)
                for _ in range(steps):
                    if animation_id != self._current_animation_id:
                        LOGGER.debug("Animation %d cancelled during hold", animation_id)
                        return
                    time.sleep(step)

            # Sau khi giữ xong, nếu vẫn là animation hiện tại thì clear màn hình và cập nhật text cũ
            if animation_id == self._current_animation_id:
                with self._lock:
                    clear_canvas = self._matrix.CreateFrameCanvas()
                    clear_canvas.Clear()
                    self._matrix.SwapOnVSync(clear_canvas)
                self._previous_text = text
            return

        # Trường hợp text cao hơn màn hình: cuộn từ dưới lên ~3 lần rồi kết thúc
        max_loops = 3
        for loop_idx in range(max_loops):
            # Nếu có animation mới, dừng ngay
            if animation_id != self._current_animation_id:
                LOGGER.debug("Animation %d cancelled before long scroll loop %d", animation_id, loop_idx)
                return

            start_offset = total_rows + text_block_height
            end_offset = -text_block_height

            for offset in range(start_offset, end_offset - 1, -1):
                if animation_id != self._current_animation_id:
                    LOGGER.debug("Animation %d cancelled mid long scroll (loop %d)", animation_id, loop_idx)
                    return

                with self._lock:
                    canvas.Clear()
                    for i, line in enumerate(lines):
                        y = baselines[i] + offset
                        # Chỉ vẽ nếu phần baseline còn nằm trong vùng hiển thị mở rộng
                        if y < -font_height or y > total_rows + font_height:
                            continue
                        graphics.DrawText(
                            canvas,
                            self._font,
                            start_x_list[i],
                            y,
                            self._text_color,
                            line,
                        )
                    self._matrix.SwapOnVSync(canvas)
                time.sleep(scroll_speed)

        # Sau khi cuộn đủ số lần, nếu chưa bị animation khác ghi đè thì cập nhật text cũ
        if animation_id == self._current_animation_id:
            self._previous_text = text
        # Không giữ frame cuối để tránh delay cho lần API tiếp theo

    def clear(self) -> None:
        if self._matrix is None:
            return
        with self._lock:
            canvas = self._matrix.CreateFrameCanvas()
            canvas.Clear()
            self._matrix.SwapOnVSync(canvas)
            self._previous_text = ""  # Xóa text cũ
            LOGGER.debug("LED display cleared")


