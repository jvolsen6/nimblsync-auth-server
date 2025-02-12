import requests
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

# Get environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
TOKEN_URL = os.getenv("TOKEN_URL")
COMPANY_ID = os.getenv("COMPANY_ID")

# Validate required environment variables
if not CLIENT_ID or not CLIENT_SECRET or not TOKEN_URL or not REFRESH_TOKEN:
    raise ValueError("❌ ERROR: Missing required environment variables. Check .env file!")

def refresh_access_token(refresh_token):
    """Refresh the QuickBooks access token using the refresh token."""
    print("🔄 Attempting to refresh access token...")

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

    print("🔍 Response Status:", response.status_code)
    print("🔍 Response Text:", response.text)

    if response.status_code == 200:
        tokens = response.json()
        new_access_token = tokens.get("access_token")
        new_refresh_token = tokens.get("refresh_token")

        if new_access_token and new_refresh_token:
            print("✅ Tokens refreshed successfully!")
            return new_access_token, new_refresh_token  # Ensure only TWO values are returned
        else:
            print("❌ Error: Missing keys in token response!")
            return None, None
    else:
        print("❌ Error refreshing token:", response.status_code, response.text)
        return None, None

def fetch_customers(access_token, company_id):
    """Fake Customer Data for Testing"""
    return [
        {"name": "Test Client 1", "company_id": "12345"},
        {"name": "Test Client 2", "company_id": "67890"},
        {"name": "Test Client 3", "company_id": "54321"},
    ]

def get_profit_and_loss(access_token, company_id, start_date, end_date):
    """Fake Profit and Loss Data for Testing"""
    fake_revenue = {
        "12345": {"2020": 50000, "2021": 70000, "2022": 90000},
        "67890": {"2020": 30000, "2021": 50000, "2022": 80000},
        "54321": {"2020": 45000, "2021": 60000, "2022": 75000},
    }
    return fake_revenue.get(company_id, {}).get(start_date[:4], 0)  # Return 0 if no data exists

# Run refresh token function if script is executed directly
if __name__ == "__main__":
    access_token, refresh_token = refresh_access_token(REFRESH_TOKEN)

    if access_token and refresh_token:
        print("\n✅ New tokens retrieved successfully.")
    else:
        print("\n❌ Failed to refresh tokens.")
