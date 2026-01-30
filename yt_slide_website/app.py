from flask import Flask, render_template, request
from slide_extractor import extract_slides
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    slides = []

    if request.method == "POST":
        yt = request.form["yt"]
        out = "static/slides"
        os.makedirs(out, exist_ok=True)

        for f in os.listdir(out):
            os.remove(os.path.join(out, f))

        extract_slides(yt, out)
        slides = os.listdir(out)

    return render_template("index.html", slides=slides)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
