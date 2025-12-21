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
        raise gr.Error("Please upload an FCM file before converting.")

    try:
        stem_source = getattr(file_obj, "name", file_obj)
        stem = Path(stem_source).stem or "converted"

        if hasattr(file_obj, "read"):
            fcm_bytes = file_obj.read()
        else:
            fcm_bytes = Path(file_obj).read_bytes()

        svg_path, _ = _fcm_bytes_to_files(fcm_bytes, stem)
        svg_preview = Path(svg_path).read_text(encoding="utf-8")
        preview_html = (
            '<style>'
            ".svg-preview-container { width: 1000px; height: 1000px; border: 1px solid #ddd; padding: 8px; "
            "display: flex; align-items: center; justify-content: center; overflow: hidden; } "
            ".svg-preview-container svg { max-width: 100%; max-height: 100%; width: 100%; height: 100%; }"
            "</style>"
            '<div class="svg-preview-container">'
            f"{svg_preview}"
            "</div>"
        )
        download_update = gr.update(value=svg_path, visible=True, interactive=True, variant="primary")
        return preview_html, download_update
    except Exception as exc:  # pragma: no cover - surfaced to UI
        raise gr.Error(f"Could not convert the file: {exc}")


with gr.Blocks(title="FCM → SVG") as demo:
    gr.Markdown(
        "# FCM → SVG Converter — "
        "<span style='font-size: 0.9em; color: #555;'>Upload an FCM file to create an SVG preview and downloadable outputs.</span>"
    )

    with gr.Row():
        with gr.Column():
            fcm_input = gr.File(label="FCM file", file_types=[".fcm"])

        with gr.Column():
            gr.Markdown("Press **Convert** to generate the SVG, then click **Download SVG** when it's ready.")

    with gr.Row():
        convert_button = gr.Button("Convert", variant="primary")
        download_button = gr.DownloadButton(
            label="Download SVG", value=None, visible=True, interactive=False, variant="secondary"
        )

    gr.Markdown("## Preview — Review the generated SVG at a scaled 1000×1000 preview before downloading.")
    svg_preview = gr.HTML(label="SVG preview")

    convert_button.click(convert_fcm, inputs=fcm_input, outputs=[svg_preview, download_button])


if __name__ == "__main__":
    demo.launch(inbrowser=True)
