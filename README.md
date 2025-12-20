# FCM Parser

This project contains my current research into writing a
free software implementation of brother's FCM format.

The data types used by the web app are documented in [fcm_format.txt].

## Features

- Read any FCM file 
- Convert any FCM file to SVG

## Web interface (Gradio)

You can run a simple local web app for converting FCM files to SVG using a Python 3.11.9 virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python gradio_app.py
```

On Windows you can launch the app (and open it automatically in your browser) with:

```
run_gradio.bat
```

The batch script activates the `venv`, runs the app, and deactivates the environment when the process ends. The app opens in your default browser via `demo.launch(inbrowser=True)`. Upload an FCM file to see the SVG preview and download both the SVG and the embedded thumbnail (`.bmp`).

## Roadmap

- Allow writing FCM files
- Rewrite the parser and serializer in Rust

SVG to FCM:
- https://stackoverflow.com/questions/734076/how-to-best-approximate-a-geometrical-arc-with-a-bezier-curve
- https://stackoverflow.com/questions/3162645/convert-a-quadratic-bezier-to-a-cubic-one

[fcm_format.txt]: docs/fcm_format.txt
