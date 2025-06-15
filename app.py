from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup as BS
import json

app = Flask(__name__)
CORS(app)


@app.route("/verify", methods=["POST"])
def verify():
    url = "http://koistudy.net"
    param = {"mid": "view_prob", "id": json.loads(request.get_data())}
    page = requests.get(url, params=param)

    if page.status_code != 200:
        return jsonify(message="error occured")
    soup = BS(page.text, "html.parser")
    text = soup.select_one("#gs13068").get_text()  # type: ignore
    res = text.split()[0]

    return jsonify(message=res)


if __name__ == "__main__":
    app.run(debug=True, port=4000)
