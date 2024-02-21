#!/usr/bin/env python3
# c-basic-offset: 4; tab-width: 8; indent-tabs-mode: nil
# vi: set shiftwidth=4 tabstop=8 expandtab:
# :indentSize=4:tabSize=8:noTabs=true:
#
# SPDX-License-Identifier: GPL-3.0-or-later
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from scopes import SCOPES

def conectar():
    """ Conectar con Google
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
        else:
          flow = InstalledAppFlow.from_client_secrets_file(
              "credentials.json", SCOPES
          )
          creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
          token.write(creds.to_json())
    return creds


def classroom_list(creds):
    """ Lista las clases que tienes
    """
    try:
        service = build("classroom", "v1", credentials=creds)

        # Call the Classroom API
        results = service.courses().list(pageSize=10).execute()
        courses = results.get("courses", [])

        if not courses:
          print("No courses found.")
          return
        # Prints the names of the first 10 courses.
        print("Courses:")
        for course in courses:
          print(course["name"])

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == '__main__':
    c = conectar()
    if c:
        classroom_list(c)
