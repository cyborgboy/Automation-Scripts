from __future__ import print_function
import time
import os.path
import ast
import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive.readonly.metadata'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

service = discovery.build('drive', 'v3', http=creds.authorize(Http()))
results = service.files().list(
        pageSize=1000,
        fields="nextPageToken, files(id, modifiedTime,  name, owners, shared)").execute()
token = results.get('nextPageToken', None)
items = results.get('files', [])

while token is not None:
    results = service.files().list(
            pageSize=1000,
            pageToken=token,
            fields="nextPageToken, files(id, modifiedTime,owners,name, shared)").execute()
    # Store the new nextPageToken on each loop iteration
    token = results.get('nextPageToken', None)
    # Append the next set of results to the items variable
    items.extend(results.get('files', []))


items_dict = ast.literal_eval(str(items))


print("You have", len(items_dict), "files in Google Drive\n")
print("The following files are shared:\n")

# Iterate through the items list and only show files that have
# shared set to True.
csv_file =  open("drive_details.csv", 'w')
headerlist = ['file_id','file_name','Lastmodified','owners']
csv_writer = csv.writer(csv_file)
csv_writer.writerow(headerlist)
for i in range(len(items_dict)):
    details = items_dict[i]['id'],items_dict[i]['name'],items_dict[i]['modifiedTime'],items_dict[i]['owners']
    if items_dict[i]['shared']:
        csv_writer.writerow(details)
        
    




