#!/usr/bin/env python3
# c-basic-offset: 4; tab-width: 8; indent-tabs-mode: nil
# vi: set shiftwidth=4 tabstop=8 expandtab:
# :indentSize=4:tabSize=8:noTabs=true:
#
# SPDX-License-Identifier: GPL-3.0-or-later
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleconn import conectar


def tarea_list(creds, course_id):
    """Lista de tareas de la clase"""
    try:
        service = build("classroom", "v1", credentials=creds)

        # Call the Classroom API
        tareas = service.courses().courseWork().list(courseId=course_id).execute()

        if not tareas:
            print("No homeworks found.")
            return
        # Prints the names of the first 10 courses.
        print("Tareas:")
        contador = 1
        while tareas.get("courseWork"):
            for t in tareas.get("courseWork"):
                print("{:>3d}".format(contador), t["id"], t["title"], t["workType"])
                contador += 1

            if not tareas.get("nextPageToken"):
                break
            tareas = (
                service.courses()
                .courseWork()
                .list(courseId=course_id, pageToken=tareas["nextPageToken"])
                .execute()
            )

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        c = conectar()
        if c:
            tarea_list(c, sys.argv[1])
    else:
        print("No course id provided.")
