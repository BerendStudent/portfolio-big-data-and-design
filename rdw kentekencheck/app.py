from flask import Flask, render_template
import requests

app = Flask(__name__)

rdw = requests.get('https://opendata.rdw.nl/resource/m9d7-ebf2.json')


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)