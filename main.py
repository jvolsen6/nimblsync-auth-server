# Main application file
from auth import generate_auth_url, exchange_code_for_token
from client_revenue import refresh_access_token
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(".env")

# Ensure required environment variables are present
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    raise ValueError("❌ ERROR: CLIENT_ID, CLIENT_SECRET, or REDIRECT_URI is missing. Check your .env file!")

def save_tokens(access_token, refresh_token):
    """Update .env file with new tokens."""
    env_lines = []
    
    with open(".env", "r") as file:
        env_lines = file.readlines()
    
    with open(".env", "w") as file:
        for line in env_lines:
            if line.startswith("ACCESS_TOKEN="):
                file.write(f"ACCESS_TOKEN={access_token}\n")
            elif line.startswith("REFRESH_TOKEN="):
                file.write(f"REFRESH_TOKEN={refresh_token}\n")
            else:
                file.write(line)
    
    print("✅ Tokens updated successfully in .env file.")

def authorize():
    """Handles the authorization process and saves tokens."""
    print("Step 1: Generate the authorization URL.")
    generate_auth_url()

    auth_code = input("Step 2: Enter the authorization code (from redirect URL): ").strip()

    print("Step 3: Exchanging authorization code for tokens...")
    tokens = exchange_code_for_token(auth_code)

    if tokens:
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]

        print("\n✅ Authorization Successful!")
        print("Access Token:", access_token)
        print("Refresh Token:", refresh_token)

        save_tokens(access_token, refresh_token)

    else:
        print("❌ Failed to exchange authorization code for tokens.")

def main():
    """Main function to refresh the access token and print updated tokens."""
    global ACCESS_TOKEN, REFRESH_TOKEN

    # Load tokens from .env
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

    if not ACCESS_TOKEN or not REFRESH_TOKEN:
        print("❌ Missing tokens. Running authorization flow...")
        authorize()
        return

    print("\n🔄 Refreshing access token...")
    tokens = refresh_access_token(REFRESH_TOKEN)

    if tokens:
        ACCESS_TOKEN, REFRESH_TOKEN = tokens
        print("✅ New Access Token:", ACCESS_TOKEN)
        print("✅ New Refresh Token:", REFRESH_TOKEN)
        save_tokens(ACCESS_TOKEN, REFRESH_TOKEN)
    else:
        print("❌ Failed to refresh tokens. Exiting program.")

if __name__ == "__main__":
    main()
