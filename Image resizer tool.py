import os
from flask import Flask, request, render_template, send_file
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if not exists

@app.route("/", methods=["GET", "POST"])
def home():
    resized_image_path = None

    if request.method == "POST":
        file = request.files["image"]
        width = int(request.form.get("width", 100))
        height = int(request.form.get("height", 100))

        if file:
            image = Image.open(file)
            resized_image = image.resize((width, height))

            filename = "resized_" + file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            resized_image.save(filepath)

            resized_image_path = filepath

    return render_template("index.html", resized_image=resized_image_path)

@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
