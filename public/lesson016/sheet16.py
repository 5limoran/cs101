"""
sheet16.py

This script should create a spreadsheet, then call 
service.spreadsheets().values().batchUpdate()

Demo:
python3 sheet16.py
"""

import datetime
import os
import pickle
from googleapiclient.discovery import build

SCOPES  = ['https://www.googleapis.com/auth/spreadsheets']
pcklf_s = os.environ['HOME']+'/secret0612.pickle'

with open(pcklf_s, 'rb') as fh:
  creds = pickle.load(fh)
            
print('OAuth session obtained from Python-pickle file:')
print(pcklf_s)

# I shd get a UTC timestamp-string for the spreadsheet title:
my_dt = datetime.datetime.utcnow()
my_s  = datetime.datetime.strftime(my_dt, '%Y-%m-%d %H:%M:%S')

title_s           = 'lesson016sheet ' + my_s
service           = build('sheets', 'v4', credentials=creds)
field_s           = 'spreadsheetUrl,spreadsheetId'
body_d            = {'properties':{'title':title_s}}
response_ofcreate = service.spreadsheets().create(fields=field_s
                                                  ,body=body_d).execute()
spreadsheet_id    = response_ofcreate.get('spreadsheetId')
print('I just created spreadsheet; it has an ID:')
print(spreadsheet_id)
spreadsheet_url = response_ofcreate.get('spreadsheetUrl')
print('spreadsheetUrl:')
print( spreadsheet_url)

range1_s  = 'Sheet1!A1' # The range in A1 notation
row1_l    = [1.1, 2.1, 3.3]
row2_l    = [1.2, 2.3, 3.1]
values1_l = [row1_l, row2_l] # A nested list full of values
d1_d      =  {'range':  range1_s, 'values': values1_l}

range2_s  = 'Sheet1!A4'
row1_l    = [1.4, 2.2, 3.1]
row2_l    = [1.1, 2.4, 3.6]
values2_l = [row1_l, row2_l]
d2_d      =  {'range':  range2_s, 'values': values2_l}

range3_s  = 'Sheet1!A7'
row1_l    = [1.4, 2.7, 3.5]
row2_l    = [1.4, 2.1, 3.1]
values3_l = [row1_l, row2_l]
d3_d      =  {'range':  range3_s, 'values': values3_l}

# I shd create a list of dictionaries:
data_l = [ d1_d, d2_d, d3_d ]

body_d = {
  'valueInputOption': 'USER_ENTERED',
  'data': data_l
} # Another dictionary for batchUpdate()

response_ofbatchUpdate = service.spreadsheets().values().batchUpdate(
  spreadsheetId=spreadsheet_id,
  body = body_d).execute()

print("response_ofbatchUpdate.get('totalUpdatedCells'):")
print( response_ofbatchUpdate.get('totalUpdatedCells')  )
