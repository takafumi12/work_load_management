# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START calendar_quickstart]
from __future__ import print_function
import datetime
import os.path
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class Get_event():

    def __init__(self, timefrom, timeto, calendarId='primary'):
        self.timefrom = timefrom
        self.timeto = timeto
        self.calendarId = calendarId

    def get_event(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        timefrom = self.timefrom
        timeto = self.timeto
        timefrom = datetime.datetime.strptime(timefrom, '%Y/%m/%d').isoformat()+'Z'
        timeto = datetime.datetime.strptime(timeto, '%Y/%m/%d').isoformat()+'Z'
        events_result = service.events().list(calendarId=self.calendarId,
                                            timeMin=timefrom,
                                            timeMax=timeto,
                                            singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        working_data = pd.DataFrame(data=None, index=None, columns=['作業詳細', '作業日', '時間'], dtype=None, copy=False)

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = datetime.datetime.strptime(start[:-6], '%Y-%m-%dT%H:%M:%S')
            end = event['end'].get('dateTime', event['end'].get('date'))
            end = datetime.datetime.strptime(end[:-6], '%Y-%m-%dT%H:%M:%S')
            work_day = end.date()
            working_time = end - start
            working_time = working_time.seconds / 3600 # 時間に変換
            tmp = pd.Series([event['summary'], str(work_day), working_time], index=working_data.columns)
            working_data = working_data.append(tmp, ignore_index=True)

        return working_data

# [END calendar_quickstart]
