from dotenv import load_dotenv
import webbrowser
import random
import requests
import string
import os
import base64

# Load environment variables
load_dotenv(".env")


# Environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
AUTH_URL = "https://appcenter.intuit.com/connect/oauth2"
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")



# Validate critical environment variables
if not CLIENT_ID or not REDIRECT_URI or not CLIENT_SECRET:
    raise ValueError("❌ ERROR: CLIENT_ID, REDIRECT_URI, or CLIENT_SECRET is not set in environment.env!")

print("✅ Environment variables loaded successfully.")

# Helper function to generate a random state string
def generate_state():
    """Generate a random state string for CSRF protection."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Generate the authorization URL
def generate_auth_url():
    """Generate the QuickBooks OAuth2 authorization URL."""
    state = generate_state()
    scopes = "com.intuit.quickbooks.accounting com.intuit.quickbooks.payment"

    # Build the authorization URL
    url = (
        f"https://appcenter.intuit.com/connect/oauth2?"
        f"client_id={CLIENT_ID}&response_type=code"
        f"&scope={scopes}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&state={state}"
    )

    print("\nAuthorization URL (open in browser):")
    print(url)
    webbrowser.open(url)
    return state



# Exchange the authorization code for access and refresh tokens
def exchange_code_for_token(auth_code):
    """Exchange the authorization code for tokens."""
    print("Auth code:", auth_code)  # Add this line to see the value of the auth_code variable

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
    print("Response:", response.text)  # Add this line to see the response from the server

    if response.status_code == 200:
        tokens = response.json()
        print("\n✅ Tokens received successfully!")
        print("Access Token:", tokens["access_token"])
        print("Refresh Token:", tokens["refresh_token"])
        return tokens
    else:
        print("\n❌ Unexpected error exchanging code for tokens:", response.status_code, response.text)
        return None

# Main flow
if __name__ == "__main__":
    # Generate the authorization URL
    state = generate_auth_url()
    print("\nGo to the authorization URL, log in, and authorize the app.")

    # Manually input the authorization code from the redirect URL
    auth_code = input("\nEnter the authorization code from the redirect URL: ").strip()
    tokens = exchange_code_for_token(auth_code)

    if tokens:
        # Save tokens to environment variables (or update them securely elsewhere)
        ACCESS_TOKEN = tokens["access_token"]
        REFRESH_TOKEN = tokens["refresh_token"]
        print("\n✅ Tokens updated successfully.")
    else:
        print("\n❌ Failed to update tokens.")
        print("Please try again with a new authorization code.")

# Refresh the access token
