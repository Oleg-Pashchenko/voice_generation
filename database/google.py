from google.oauth2 import service_account
from googleapiclient.discovery import build
from misc.secrets import secret_info

creds = service_account.Credentials.from_service_account_file(secret_info.GOOGLE_SHEET.GOOGLE_AUTH_FILE_NAME)
service = build('sheets', 'v4', credentials=creds)
spreadsheet_id = secret_info.GOOGLE_SHEET.GOOGLE_SPREADSHEET_ID
range_name = secret_info.GOOGLE_SHEET.GOOGLE_SHEET_NAME
result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
print(result)
