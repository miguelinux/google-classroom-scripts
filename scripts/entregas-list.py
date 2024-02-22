#!/usr/bin/env python3
# c-basic-offset: 4; tab-width: 8; indent-tabs-mode: nil
# vi: set shiftwidth=4 tabstop=8 expandtab:
# :indentSize=4:tabSize=8:noTabs=true:
#
# SPDX-License-Identifier: GPL-3.0-or-later
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleconn import conectar


def entregas_list(creds, course_id, work_id):
    """Lista de entregas de tarea de la clase"""
    entregas = []
    page_token = None

    try:
        service = build("classroom", "v1", credentials=creds)

        # Call the Classroom API
        ss = service.courses().courseWork().studentSubmissions()

        # Prints the names of the first 10 courses.
        print("Entregas:")
        while True:
            lista = ss.list(
                courseId=course_id, courseWorkId=work_id, pageToken=page_token
            ).execute()

            if not lista:
                print("No entregas found.")
                break

            entregas.extend(lista.get("studentSubmissions", []))

            page_token = lista.get("nextPageToken", None)
            if not page_token:
                break

        contador = 1
        for e in entregas:
            print(
                "{:>3d}".format(contador),
                e.get("userId") + ":",
                e.get("assignedGrade", "NC"),
                end=":",
            )
            sa = e.get("shortAnswerSubmission", None)
            if sa:
                saa = sa.get("answer", None)
                if saa:
                    print(saa, end="")
            print()
            contador += 1

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        c = conectar()
        if c:
            entregas_list(c, sys.argv[1], sys.argv[2])
    else:
        print("No course id or course work id provided.")
