#!/usr/bin/env python3
# c-basic-offset: 4; tab-width: 8; indent-tabs-mode: nil
# vi: set shiftwidth=4 tabstop=8 expandtab:
# :indentSize=4:tabSize=8:noTabs=true:
#
# SPDX-License-Identifier: GPL-3.0-or-later
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleconn import conectar


def classroom_list(creds):
    """Lista las clases que tienes"""
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
            if course["courseState"] == "ACTIVE":
                print(course["id"], ":", "{:>50s}".format(course["name"]))

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    c = conectar()
    if c:
        classroom_list(c)
