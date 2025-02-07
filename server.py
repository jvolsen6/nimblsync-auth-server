import os
import requests
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

# Environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

@app.route("/")
def home():
    return "NimblSync OAuth Server is Running!"

@app.route("/auth/callback")
def auth_callback():
    """Handles QuickBooks OAuth2 callback and exchanges the code for an access token."""
    auth_code = request.args.get("code")
    state = request.args.get("state")

    if not auth_code:
        return "Error: No authorization code received.", 400

    # Exchange authorization code for access token
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
        return jsonify({
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"]
        })
    else:
        return f"Error exchanging code: {response.text}", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
