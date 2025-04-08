from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route("/verify", methods=["GET"])
def verify():
    return jsonify(message="Hello, World")


if __name__ == "__main__":
    app.run(debug=True, port=4000)
