from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Replace with your Google Cloud project ID
PROJECT_ID = "cleaning-bot-432613"

# Replace with the path to your service account key file
SERVICE_ACCOUNT_FILE = "cleaning-bot-432613-43d5560b57a5.json"

# Replace with the spreadsheet ID
SPREADSHEET_ID = "141XMzYf8kJkWdwuNqsdjuCQirxXaFEqGuCMRlWCJAlo"

# Define the scope for accessing Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Create credentials using the service account key file
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Google Sheets API service
service = build("sheets", "v4", credentials=creds)

# Define the sheet name
SHEET_NAME = "Sheet1"  # Replace with your sheet name

def write_data_to_sheet(data):
    """Writes data to the specified Google Sheet.

    Args:
        data: A list of lists representing the data to write.
    """
    try:
        # Define the range to write to
        range_ = f"{SHEET_NAME}!A1:Z100"  # Adjust the range as needed

        # Write the data to the sheet
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_,
            valueInputOption="RAW",
            body={"values": data},
        ).execute()

        print(f"Data written to sheet: {SHEET_NAME}")


    except HttpError as error:
        print(f"An error occurred: {error}")

# Example usage:
data = [
    ["Name", "Age", "City"],
    ["John Doe", 30, "New York"],
    ["Jane Doe", 25, "London"],
]

write_data_to_sheet(data)
