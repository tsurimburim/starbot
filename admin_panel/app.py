
from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route("/")
def dashboard():
    with open("data.json", "r") as f:
        users = json.load(f)
    return render_template("index.html", users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
