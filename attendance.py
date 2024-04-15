import numpy as np




def generate(
    count,
    excusedProb,
    lateProb,
    attendanceProb,
    catchupTasks,
    df_meetings,
    df_students,
    df_teachers,
    df_courses,
):

    df = df_meetings.merge(df_students, on="ClassName")
    df = df.rename(columns={"Name": "StudentName", "Surname": "StudentSurname"})
    df = df.merge(df_courses, on="cID")
    df = df.rename(columns={"Name": "CourseName"})
    df = df.merge(df_teachers, on="tID")
    df = df.rename(columns={"Name": "TeacherName", "Surname": "TeacherSurname"})

    df = df[
        np.random.choice(
            [True, False], size=len(df), p=[1 - attendanceProb, attendanceProb]
        )
    ]

    df["Excused"] = np.random.choice(
        [True, False], size=len(df), p=[excusedProb, 1 - excusedProb]
    )
    df["Late"] = np.random.choice(
        [True, False], size=len(df), p=[lateProb, 1 - lateProb]
    )
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
    if count > len(df):
        count = len(df)

    if count > 0:
        df = df.sample(n=count, replace=True)

    return df
