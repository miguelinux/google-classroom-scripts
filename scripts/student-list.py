#!/usr/bin/env python3
# c-basic-offset: 4; tab-width: 8; indent-tabs-mode: nil
# vi: set shiftwidth=4 tabstop=8 expandtab:
# :indentSize=4:tabSize=8:noTabs=true:
#
# SPDX-License-Identifier: GPL-3.0-or-later
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleconn import conectar


def student_list(creds, course_id):
    """Lista de alumnos de la clase"""
    try:
        service = build("classroom", "v1", credentials=creds)

        # Call the Classroom API
        students = service.courses().students().list(courseId=course_id).execute()

        if not students:
            print("No students found.")
            return
        # Prints the names of the first 10 courses.
        print("Alumnos:")
        contador = 1
        while True:
            for s in students["students"]:
                print(
                    "{:>3d}".format(contador),
                    s["profile"]["id"] + ":",
                    s["profile"]["name"]["fullName"],
                )
                contador += 1

            if not students.get("nextPageToken"):
                break
            students = (
                service.courses()
                .students()
                .list(courseId=course_id, pageToken=students["nextPageToken"])
                .execute()
            )

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        c = conectar()
        if c:
            student_list(c, sys.argv[1])
    else:
        print("No course id provided.")
