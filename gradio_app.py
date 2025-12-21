import io
import tempfile
from pathlib import Path

import gradio as gr

from fcm import generate_svg, read_fcm_file


def _fcm_bytes_to_files(fcm_bytes: bytes, stem: str) -> tuple[str, str]:
    """Convert FCM bytes to SVG and thumbnail files, returning their paths."""
    parsed = read_fcm_file(fcm_bytes)

    temp_dir = Path(tempfile.mkdtemp())
    svg_path = temp_dir / f"{stem}.svg"
    thumbnail_path = temp_dir / f"{stem}.bmp"

    svg_buffer = io.StringIO()
    generate_svg(svg_buffer, parsed)
    svg_path.write_text(svg_buffer.getvalue(), encoding="utf-8")
    thumbnail_path.write_bytes(parsed.file_header.thumbnail_bytes)

    return str(svg_path), str(thumbnail_path)


def convert_fcm(file_obj):
    """Gradio callback to convert an uploaded FCM file to SVG."""
    if file_obj is None:
        raise gr.Error("Пожалуйста, загрузите FCM файл.")

    try:
        stem_source = getattr(file_obj, "name", file_obj)
        stem = Path(stem_source).stem or "converted"

        if hasattr(file_obj, "read"):
            fcm_bytes = file_obj.read()
        else:
            fcm_bytes = Path(file_obj).read_bytes()

        svg_path, thumbnail_path = _fcm_bytes_to_files(fcm_bytes, stem)
        svg_preview = Path(svg_path).read_text(encoding="utf-8")
        preview_html = (
            '<div style="max-height: 640px; overflow: auto; border: 1px solid #ddd; padding: 8px;">'
            f"{svg_preview}"
            "</div>"
        )
        return preview_html, svg_path, thumbnail_path
    except Exception as exc:  # pragma: no cover - surfaced to UI
        raise gr.Error(f"Не удалось конвертировать файл: {exc}")


with gr.Blocks(title="FCM → SVG") as demo:
    gr.Markdown(
        """
        # Конвертер FCM → SVG

        Загрузите файл формата FCM, чтобы получить SVG и встроенный превью.
        """
    )

    with gr.Row():
        fcm_input = gr.File(label="FCM файл", file_types=[".fcm"])
        convert_button = gr.Button("Конвертировать")

    svg_preview = gr.HTML(label="SVG превью")
    svg_file = gr.File(label="Скачать SVG")
    thumbnail_file = gr.File(label="Скачать миниатюру BMP")

    convert_button.click(convert_fcm, inputs=fcm_input, outputs=[svg_preview, svg_file, thumbnail_file])


if __name__ == "__main__":
    demo.launch(inbrowser=True)
