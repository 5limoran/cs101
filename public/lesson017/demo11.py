"""
demo11.py

This script should:

- Create a spreadsheet named hello spreadsheet
- Write some rows into it
- Grant reader-role to anyone (who wants it)
- Grant writer-role to bikle101@gmail.com

Demo:
python3 demo11.py
"""

import datetime
import os
import pickle
from googleapiclient.discovery    import build
from googleapiclient.http         import MediaFileUpload
from oauth2client.service_account import ServiceAccountCredentials
from httplib2                     import Http

secretf_s = os.environ['HOME']+'/secret0616.json'

with open(secretf_s) as fh:
  json_s = fh.read()

print('json_s[:66]:')
print( json_s[:66])

# I s.declare a very permissive scope (for training only):
SCOPES      = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(secretf_s,
                                                               SCOPES)
http_auth = credentials.authorize(Http())
service   = build('sheets', 'v4', http=http_auth)

print('I should now be authenticated and authorized to use service:')
print(service)

field_s           = 'spreadsheetId,spreadsheetUrl'
body_d            = {'properties':{'title':'hello spreadsheet'}}

response_ofcreate = service.spreadsheets().create(fields=field_s, body=body_d).execute()

spreadsheet_id    = response_ofcreate.get('spreadsheetId')

print('I just created spreadsheet; it has an ID:')
print(spreadsheet_id)
spreadsheet_url = response_ofcreate.get('spreadsheetUrl')
print('spreadsheetUrl:')
print( spreadsheet_url)

# I shd add some data to the spreadsheet:

range_s  = 'Sheet1!A1' # The range in A1 notation
row1_l   = [1.1, 2.1, 3.3]
row2_l   = [1.2, 2.3, 3.1]
values_l = [row1_l, row2_l] # A nested list full of values
body     = {'values': values_l}

response_ofupdate = service.spreadsheets().values().update(
    spreadsheetId=spreadsheet_id, range=range_s,
    valueInputOption='USER_ENTERED', body=body).execute()

print("response_ofupdate.get('updatedCells'):")
print( response_ofupdate.get('updatedCells')  )
print('response_ofupdate:')
print( response_ofupdate)

# I shd grant reader-role to anyone (who wants it):
newperm_d     = {'role': 'reader', 'type': 'anyone'}
drive_service = build('drive', 'v3', http=http_auth)
pc_response   = drive_service.permissions().create(fileId=spreadsheet_id,
                                                   body=newperm_d
).execute()

print('pc_response:')
print( pc_response)

# I shd grant writer-role to bikle101@gmail.com:
newperm_d   = {'role': 'writer', 'type': 'user',
               'emailAddress': 'bikle101@gmail.com'}

pc_response = drive_service.permissions().create(fileId=spreadsheet_id,
                                                 body=newperm_d
).execute()

print('pc_response:')
print( pc_response)

