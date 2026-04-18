from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# Video Upload Route
@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("video")

    if not file:
        return jsonify({"status":"error","message":"No file selected"})

    filename = file.filename

    return jsonify({
        "status":"success",
        "message":"Video uploaded successfully",
        "filename": filename
    })

# YouTube Link Route
@app.route("/youtube", methods=["POST"])
def youtube():

    data = request.get_json()

    link = data.get("link")

    if not link:
        return jsonify({"status":"error","message":"No link found"})

    return jsonify({
        "status":"success",
        "message":"YouTube link received",
        "link": link
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
