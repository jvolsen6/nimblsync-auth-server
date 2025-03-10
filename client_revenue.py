import os
import json
import csv
import requests
import base64
from dotenv import load_dotenv
from auth import refresh_access_token  # Import refresh_access_token from auth.py

# Load environment variables
load_dotenv(".env")

# Get environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
COMPANY_ID = os.getenv("COMPANY_ID")
TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"

def update_env_file(access_token, refresh_token):
    """Safely update the .env file with new tokens."""
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

def save_to_csv(data, output_file="output/client_revenue.csv"):
    """Save the client revenue data to a CSV file."""
    if not data:
        print("❌ No revenue data to save. Skipping CSV writing.")
        return

    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Ensure output directory exists

    try:
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Client Name", "Company ID", "Year", "Revenue"])  # Write headers
            
            for row in data:
                writer.writerow([row["client_name"], row["company_id"], row["year"], row["revenue"]])
        
        print(f"✅ Data saved successfully to {output_file}.")
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")

def fetch_customers():
    """Fake Customer Data for Testing."""
    return [
        {"name": "Test Client 1", "company_id": "12345"},
        {"name": "Test Client 2", "company_id": "67890"},
        {"name": "Test Client 3", "company_id": "54321"},
    ]

def get_profit_and_loss(access_token, company_id, start_date, end_date):
    """Fake Profit and Loss Data for Testing."""
    fake_revenue = {
        "12345": {"2020": 50000, "2021": 70000, "2022": 90000},
        "67890": {"2020": 30000, "2021": 50000, "2022": 80000},
        "54321": {"2020": 45000, "2021": 60000, "2022": 75000},
    }
    return fake_revenue.get(company_id, {}).get(start_date[:4], 0)  # Return 0 if no data exists

def main():
    global ACCESS_TOKEN, REFRESH_TOKEN

    print("🔄 Refreshing access token...")
    tokens = refresh_access_token(REFRESH_TOKEN)  # Use function from auth.py

    if tokens and len(tokens) == 2:  # Ensure we have exactly 2 values before unpacking
        ACCESS_TOKEN, REFRESH_TOKEN = tokens
        update_env_file(ACCESS_TOKEN, REFRESH_TOKEN)  # Save new tokens to .env
    else:
        print("❌ Failed to refresh tokens. Exiting program.")
        return

    print("🔍 Fetching customer data from QuickBooks...")
    customers = fetch_customers()

    if not customers:
        print("❌ No customer data retrieved. Exiting.")
        return

    print(f"✅ Fetched {len(customers)} customers.")

    revenue_data = []
    years = ["2020", "2021", "2022"]

    for client in customers:
        client_name = client["name"]
        company_id = client["company_id"]
        print(f"\n📊 Fetching financial data for {client_name} (Company ID: {company_id})...")

        for year in years:
            start_date = f"{year}-01-01"
            end_date = f"{year}-12-31"
            revenue = get_profit_and_loss(ACCESS_TOKEN, company_id, start_date, end_date)

            if revenue is not None:
                print(f"  ✅ Year {year}: Revenue = {revenue}")
                revenue_data.append({
                    "client_name": client_name,
                    "company_id": company_id,
                    "year": year,
                    "revenue": revenue,
                })
            else:
                print(f"  ❌ No data available for {client_name} in {year}.")

    print("\n💾 Saving revenue data to CSV...")
    save_to_csv(revenue_data)

if __name__ == "__main__":
    main()
