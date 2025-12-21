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

        svg_path, thumbnail_path = _fcm_bytes_to_files(fcm_bytes, stem)
        svg_preview = Path(svg_path).read_text(encoding="utf-8")
        preview_html = (
            '<div style="max-height: 640px; overflow: auto; border: 1px solid #ddd; padding: 8px;">'
            f"{svg_preview}"
            "</div>"
        )
        download_update = gr.DownloadButton.update(value=svg_path, visible=True)
        return preview_html, download_update, thumbnail_path
    except Exception as exc:  # pragma: no cover - surfaced to UI
        raise gr.Error(f"Could not convert the file: {exc}")


with gr.Blocks(title="FCM → SVG") as demo:
    gr.Markdown(
        """
        # FCM → SVG Converter

        Upload an FCM file to create an SVG preview and downloadable outputs.
        """
    )

    with gr.Row():
        with gr.Column():
            fcm_input = gr.File(label="FCM file", file_types=[".fcm"])
            gr.Markdown("Upload your FCM (.fcm) design file here before starting conversion.")

        with gr.Column():
            convert_button = gr.Button("Convert")
            gr.Markdown("Click **Convert** after uploading to generate the SVG and preview.")

    gr.Markdown("## Preview")
    gr.Markdown("Review the generated SVG. Scroll to inspect the full design before downloading.")
    svg_preview = gr.HTML(label="SVG preview")

    gr.Markdown("## Downloads")
    gr.Markdown("Download the converted SVG or the BMP thumbnail created from your FCM file.")
    download_svg = gr.DownloadButton(label="Download SVG", value=None, visible=False)
    thumbnail_file = gr.File(label="Download BMP thumbnail")

    convert_button.click(convert_fcm, inputs=fcm_input, outputs=[svg_preview, download_svg, thumbnail_file])


if __name__ == "__main__":
    demo.launch(inbrowser=True)
