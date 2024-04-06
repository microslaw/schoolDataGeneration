import numpy as np

defaultCatchupTasks = [
    "Read pages 1-10",
    "Do exercises 1-5",
    "Read pages 11-20",
    "Do exercises 6-10",
    "Read pages 21-30",
    "Do exercises 11-15",
    "Read pages 31-40",
    "Do entire page 41",
    "Do tasks 5 and 7a from page 42",
    "Write a summary of the chapter",
    "None",
]


def generate(count, meetings, students, teachers, courses, exusedProb=0.7, lateProb=0.2, attendanceProb = 0.99, catchupTasks=defaultCatchupTasks):

    df = meetings.merge(students, on="ClassName")
    df = df.rename(columns={"Name": "StudentName", "Surname": "StudentSurname"})
    df = df.merge(courses, on="cID")
    df = df.rename(columns={"Name": "CourseName"})
    df = df.merge(teachers, on="tID")
    df = df.rename(columns={"Name": "TeacherName", "Surname": "TeacherSurname"})

    df = df[ np.random.choice([True, False], size=len(df), p=[1 - attendanceProb, attendanceProb])]

    df["Excused"] = np.random.choice([True, False], size=len(df), p=[exusedProb, 1 - exusedProb])
    df["Late"] = np.random.choice([True, False], size=len(df), p=[lateProb, 1 - lateProb])
    df["CatchUp"] = np.random.choice(catchupTasks, size=len(df))
    df["StartHour"] = df["StartHour"].astype(str) + ":00"
    df["EndHour"] = df["EndHour"].astype(str) + ":00"


    df = df[
        [
            "StudentName",
            "StudentSurname",
            "sID",
            "ClassName",
            "StartHour",
            "EndHour",
            "CourseName",
            "mID",
            "TeacherName",
            "TeacherSurname",
            "tID",
            "Excused",
            "CatchUp",
            "Late",
        ]
    ]

    return df
