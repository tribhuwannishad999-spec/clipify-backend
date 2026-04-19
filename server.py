from flask import Flask, render_template, request, jsonify, send_file
import os
import subprocess
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


# =========================
# VIDEO UPLOAD TO SHORTS
# =========================
@app.route("/upload", methods=["POST"])
def upload():

    try:
        file = request.files.get("video")

        if not file:
            return jsonify({"status": "error", "message": "No file selected"})

        uid = str(uuid.uuid4())[:8]

        input_path = os.path.join(UPLOAD_FOLDER, uid + "_" + file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, uid + "_short.mp4")

        file.save(input_path)

        cmd = [
            "ffmpeg",
            "-i", input_path,

            # first 15 sec clip
            "-ss", "00:00:00",
            "-t", "15",

            # vertical shorts format
            "-vf",
            "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,eq=contrast=1.08:brightness=0.03:saturation=1.25",

            # audio keep
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "192k",

            "-movflags", "+faststart",
            "-y",
            output_path
        ]

        subprocess.run(cmd, check=True)

        return send_file(
            output_path,
            as_attachment=True,
            download_name="clipify_short.mp4"
        )

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Failed to process video",
            "error": str(e)
        })


# =========================
# YOUTUBE LINK DEMO ROUTE
# =========================
@app.route("/youtube", methods=["POST"])
def youtube():

    try:
        data = request.get_json()
        link = data.get("link")

        if not link:
            return jsonify({"status": "error", "message": "No link found"})

        return jsonify({
            "status": "success",
            "message": "YouTube link accepted. Downloader setup next phase.",
            "link": link
        })

    except:
        return jsonify({"status": "error", "message": "Invalid request"})


# =========================
# HEALTH CHECK
# =========================
@app.route("/health")
def health():
    return "Clipify AI Backend Running"


# =========================
# START
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
