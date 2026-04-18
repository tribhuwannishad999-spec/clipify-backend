# server.py
from flask import Flask, render_template, request, jsonify, send_file
import os, subprocess, uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("video")

    if not file:
        return jsonify({"status":"error","message":"No file selected"}), 400

    uid = str(uuid.uuid4())[:8]
    input_path = os.path.join(UPLOAD_FOLDER, uid + "_" + file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, uid + "_short.mp4")

    file.save(input_path)

    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-ss", "00:00:00",
        "-t", "15",
        "-vf", "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-y",
        output_path
    ]

    try:
        subprocess.run(cmd, check=True)
        return send_file(output_path, as_attachment=True)
    except:
        return jsonify({"status":"error","message":"Processing failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
