from flask import Flask, request, jsonify, redirect
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_URL = os.getenv("TOKEN_URL")

@app.route("/")
def home():
    return "QuickBooks OAuth Test App is running!"

@app.route("/auth/callback", methods=["GET"])
def auth_callback():
    auth_code = request.args.get("code")
    state = request.args.get("state")

    if not auth_code:
        return "Authorization code not provided", 400

    # Exchange auth_code for tokens
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_header = base64.b64encode(auth_string.encode()).decode()

    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    if response.status_code == 200:
        tokens = response.json()
        return jsonify(tokens)  # Return tokens for testing
    else:
        return f"Token exchange failed: {response.status_code}, {response.text}", 400

if __name__ == "__main__":
    app.run(debug=True)
