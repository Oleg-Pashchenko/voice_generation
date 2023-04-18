from dotenv import load_dotenv
import os
import dataclasses





@dataclasses.dataclass
class GoogleSheetInformation:
    GOOGLE_AUTH_FILE_NAME: str
    GOOGLE_SPREADSHEET_ID: str
    GOOGLE_SHEET_NAME: str


@dataclasses.dataclass
class SecretInformation:
    GOOGLE_SHEET: GoogleSheetInformation
    ZVUKOGRAM_API_KEY: str
    YANDEX_API_KEY: str
    AZURE_API_KEY: str



load_dotenv()
secret_info = SecretInformation(
    GOOGLE_SHEET=GoogleSheetInformation(
        os.getenv('GOOGLE_AUTH_FILE_NAME'),
        os.getenv('GOOGLE_SPREADSHEET_ID'),
        os.getenv('GOOGLE_SHEET_NAME')
    ),
    ZVUKOGRAM_API_KEY=os.getenv('ZVUKOGRAM_API_KEY'),
    YANDEX_API_KEY=os.getenv('YANDEX_SECRET_KEY'),
    AZURE_API_KEY=os.getenv('AZURE_SECRET_KEY')
)
