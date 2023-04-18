from google.oauth2 import service_account
from googleapiclient.discovery import build

from database.models import CreationTask, Voice
from misc.secrets import secret_info

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_table():
    creds = service_account.Credentials.from_service_account_file(secret_info.GOOGLE_SHEET.GOOGLE_AUTH_FILE_NAME)
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = secret_info.GOOGLE_SHEET.GOOGLE_SPREADSHEET_ID
    range_name = secret_info.GOOGLE_SHEET.GOOGLE_SHEET_NAME
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result['values']
    headers = values[0]
    table_dict = {}
    for row in values[1:]:
        key = row[2]
        values = row[3:25]
        table_dict[key] = values
    return table_dict, result['values']


def get_navigation_settings(table_dict):
    settings = table_dict['Navigation_settings']
    response = []
    for setting in settings:
        d = {}
        setting = setting.strip().split('\n')
        for s in setting:
            k, v = map(str, s.split('='))
            v = v.replace("'", '')
            if ';' in v:
                v = v.split(';')
            d[k] = v
        response.append(d)
    return response


def get_creation_task(s, table, x) -> CreationTask:
    if True:
        video_name_source = table[int(s['Video_source']) - 1][x]
        video_name = table[int(s['Final_video']) - 1][x]
        audio_name_source = table[int(s['Audio_source']) - 1][x]
        audio_name = table[int(s['Final_audio']) - 1][x]
        folder_path = table[int(s['Maternal_catalog']) - 1][x]
        folder_name = table[int(s['Release_folder']) - 1][x]
        voice_settings = table[int(s['Voice_settings']) - 1][x]
        voice_service = voice_settings.split("service='")[1].split("'")[0]
        voice_language = voice_settings.split("language='")[1].split("'")[0]
        voice_speaker = voice_settings.split("speaker='")[1].split("'")[0]
        voice_speed = float(voice_settings.split("speed='")[1].split("'")[0])
        voice_tone = float(voice_settings.split("tone='")[1].split("'")[0])
        voice_emotion = voice_settings.split("emotion='")[1].split("'")[0]
        pause_symbol = table[int(s['Pause_symbol']) - 1][x].split("='")[1].split("'")[0]
        text_start, text_finish = map(int, s['Text_settings'].split(':'))
        text = []
        for t in range(text_start - 1, text_finish):
            try:
                text.append(table[t][x])
            except:
                pass
        correction_of_pauses_in_the_voice = int(table[int(s['Correction_of_pauses_in_the_voice']) - 1][x].split("='")[1].split("'")[0])
        pauses_between_segments = int(table[int(s['Pauses_between_segments']) - 1][x].split("='")[1].split("'")[0])
        return CreationTask(audio_name=audio_name,
                            audio_name_source=audio_name_source,
                            video_name=video_name,
                            video_name_source=video_name_source,
                            voice=Voice(
                                service=voice_service,
                                language=voice_language,
                                speaker=voice_speaker,
                                speed=voice_speed,
                                tone=voice_tone,
                                emotion=voice_emotion
                            ),
                            pause_symbol=pause_symbol,
                            pauses_between_segments=pauses_between_segments,
                            text=text,
                            correction_of_pauses_in_the_voice=correction_of_pauses_in_the_voice
                            )


def get_tasks():
    tasks = []
    table, data = get_table()
    settings = get_navigation_settings(table)
    x = 2
    for setting in settings:
        x += 1
        task = get_creation_task(setting, data, x)
        tasks.append(task)
    return tasks


def write_stats(result):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(secret_info.GOOGLE_SHEET.GOOGLE_AUTH_FILE_NAME, scope)
    client = gspread.authorize(creds)
    sheet = client.open('Distribution').get_worksheet(1)
    row_values = sheet.row_values(2)
    col_values = sheet.col_values(2)
    cell_list = []
    for res in result:
        if res[0] != 0:
            language = res[2].split('_')[-1].split('.')[0]
            for k, v in res[1].items():
                segment = f"Сегмент - {k.split('_')[0]}"
                cell_list.append(gspread.Cell(col_values.index(segment) + 1, row_values.index(language) + 1, v))
    sheet.update_cells(cell_list)