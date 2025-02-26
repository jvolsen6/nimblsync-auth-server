from dotenv import load_dotenv
import webbrowser
import random
import requests
import string
import os
import base64
from flask import Flask, request

app = Flask(__name__)

@app.route('/auth/callback')
def auth_callback():
    return "Flask is running!"


# Load environment variables
load_dotenv(".env")

# Environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
AUTH_URL = "https://appcenter.intuit.com/connect/oauth2"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

# Validate critical environment variables
if not CLIENT_ID or not REDIRECT_URI or not CLIENT_SECRET:
    raise ValueError("❌ ERROR: CLIENT_ID, REDIRECT_URI, or CLIENT_SECRET is missing. Check your .env file!")

print("✅ Environment variables loaded successfully.")

# Helper function to generate a random state string
def generate_state():
    """Generate a random state string for CSRF protection."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Save tokens to .env file securely
def save_tokens(access_token, refresh_token):
    """Update .env file with new tokens."""
    try:
        with open(".env", "r") as file:
            lines = file.readlines()

        with open(".env", "w") as file:
            for line in lines:
                if line.startswith("ACCESS_TOKEN="):
                    file.write(f"ACCESS_TOKEN={access_token}\n")
                elif line.startswith("REFRESH_TOKEN="):
                    file.write(f"REFRESH_TOKEN={refresh_token}\n")
                else:
                    file.write(line)

        print("✅ Tokens updated successfully in .env file.")
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")

# Generate the authorization URL
def generate_auth_url():
    state = "xyz"  # Any random string for CSRF protection
    scopes = "com.intuit.quickbooks.accounting"
    auth_url = (
        f"https://appcenter.intuit.com/connect/oauth2?"
        f"client_id={CLIENT_ID}&response_type=code&scope={scopes}"
        f"&redirect_uri={REDIRECT_URI}&state={state}"
    )
    print("Authorization URL:", auth_url)
    webbrowser.open(auth_url)  # Automatically open the URL in the default browser
    return auth_url



# Exchange the authorization code for access and refresh tokens
def exchange_code_for_token(auth_code):
    """Exchange the authorization code for tokens."""
    print("🔄 Exchanging authorization code for tokens...")

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
    print("🔍 Response:", response.text)  

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]

        print("\n✅ Tokens received successfully!")
        print("Access Token:", access_token)
        print("Refresh Token:", refresh_token)

        save_tokens(access_token, refresh_token)  # Save tokens securely
        return tokens
    else:
        print("\n❌ Error exchanging code for tokens:", response.status_code, response.text)
        return None

# Refresh the access token using the refresh token
import requests
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

# Get environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

def refresh_access_token(refresh_token):
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_header = base64.b64encode(auth_string.encode()).decode()

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(TOKEN_URL, data=payload, headers=headers)

    if response.status_code == 200:
        tokens = response.json()
        print("New Access Token:", tokens["access_token"])
        print("New Refresh Token:", tokens["refresh_token"])
    else:
        print(f"Failed to refresh token: {response.status_code}, {response.text}")

# Main flow
if __name__ == "__main__":
    print("\n🔹 Select an option:")
    print("1️⃣ Generate authorization URL")
    print("2️⃣ Refresh access token")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()

    if choice == "1":
        state = generate_auth_url()
        print("\nGo to the authorization URL, log in, and authorize the app.")

        auth_code = input("\nEnter the authorization code from the redirect URL: ").strip()
        tokens = exchange_code_for_token(auth_code)

        if tokens:
            print("\n✅ Tokens updated successfully.")
        else:
            print("\n❌ Failed to update tokens. Try again.")

    elif choice == "2":
        if not REFRESH_TOKEN:
            print("\n❌ ERROR: No refresh token found. Run authorization first.")
        else:
            access_token, refresh_token = refresh_access_token(REFRESH_TOKEN)

            if access_token and refresh_token:
                print("\n✅ Tokens refreshed successfully.")
            else:
                print("\n❌ Failed to refresh tokens.")
    else:
        print("\n❌ Invalid choice. Please enter 1 or 2.")
