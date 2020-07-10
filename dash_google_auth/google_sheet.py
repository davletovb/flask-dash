from __future__ import print_function

import datetime
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
APPLICATION_NAME = "Google Sheets API Python"

SPREADSHEET_ID = "ID"


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            flow.user_agent = APPLICATION_NAME
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    sheet_name, column, size = get_range(sheet)
    start_row = 2
    end_row = size
    working_range = sheet_name + "!C" + str(start_row) + ":D" + str(end_row)
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=working_range).execute()
    values = result.get('values', [])

    results = []

    for i, row in enumerate(values):
        print(datetime.datetime.now().strftime("%H:%M:%S") + " - " + str(i) + " - " + row[1])
        if row[0] == 'Telegram':
            url = row[1]
            results.append("")
        elif row[0] == 'OK':
            url = row[1]
            results.append("")
        else:
            results.append("")

    save_to_sheet(sheet, sheet_name + "!" + column + str(start_row) + ":" + column + str(end_row), results)
    save_date(sheet, sheet_name + "!" + column + str(1))


def save_to_sheet(sheet, range_name, values):
    body = {'values': [values], 'majorDimension': 'COLUMNS'}
    result = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=range_name, valueInputOption="USER_ENTERED",
                                   body=body).execute()
    print('{} cells updated.'.format(result.get('updatedCells')))


def save_date(sheet, range_name):
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    result = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=range_name, valueInputOption="USER_ENTERED",
                                   body={"values": [[date]]}).execute()
    print('{} cells updated.'.format(result.get('updatedCells')))


def get_range(sheet):
    result = sheet.get(spreadsheetId=SPREADSHEET_ID,
                       fields='sheets(data/rowData/values/userEnteredValue,properties(index,sheetId,title))').execute()
    sheet_index = 0
    sheet_name = result['sheets'][sheet_index]['properties']['title']
    last_row = len(result['sheets'][sheet_index]['data'][0]['rowData']) + 1
    last_column_number = max([len(e['values']) for e in result['sheets'][sheet_index]['data'][0]['rowData'] if e])
    X = lambda n: ~int(n) and X(int(n / 26) - 1) + chr(65 + n % 26) or ''
    last_column = X(last_column_number)
    size = [sheet_name, last_column, last_row]
    return size


if __name__ == '__main__':
    main()
