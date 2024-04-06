import pandas as pd
import random
import numpy as np
import time
from datetime import timedelta, datetime
from utils import generateDates
from itertools import product


def isRoomFree(df, room, startHour, endHour):
    df = df[df["RoomNumber"] == room]
    df = df[df["EndHour"] > startHour]
    df = df[df["StartHour"] < endHour]

    if len(df) > 0:
        return False
    return True


def isClassFree(df, cID, startHour, endHour):
    df = df[df["cID"] == cID]
    df = df[df["EndHour"] > startHour]
    df = df[df["StartHour"] < endHour]

    if len(df) > 0:
        return False
    return True


def isTeacherFree(df, tID, startHour, endHour):
    df = df[df["tID"] == tID]
    df = df[df["EndHour"] > startHour]
    df = df[df["StartHour"] < endHour]

    if len(df) > 0:
        return False
    return True


def scheduleClassDay(df, courses, aClass, aClassCourses, rooms, schoolStart, schoolEnd):
    """
    aClass is id of a class that has schedule made for them
    aClassCourses is a list of courses that the class has
    courses is a dataframe with all courses
    """

    schedule = pd.DataFrame(columns=["RoomNumber", "StartHour", "EndHour", "cID", "tID"])
    start_times = range(schoolStart, schoolEnd + 1)
    room_numbers = rooms["RoomNumber"].tolist()
    combinations = list(product(start_times, room_numbers))

    random.shuffle(combinations)
    courses = courses[courses["cID"].isin(aClassCourses)]
    for index, row in courses[["cID", "tID"]].iterrows():
        for start, room in combinations:
            if (isRoomFree(df, room, start, start + 1) and
                isClassFree(df, aClass, start, start + 1) and
                isTeacherFree(df, row["tID"], start, start + 1)):
                schedule.loc[len(schedule) + len(df)] = {
                    "RoomNumber": room,
                    "StartHour": start,
                    "EndHour": start + 1,
                    "cID": row["cID"],
                    "tID": row["tID"],
                }
                break
        else:
            print("No available schedule found for this course.")
    return schedule


dfBase = pd.DataFrame(
    columns=[
        "Date",
        "RoomNumber",
        "StartHour",
        "EndHour",
        "cID",
        "tID",
        "ClassName",
    ]
)

dailyScheduleBase = pd.DataFrame(
    columns=[
        "RoomNumber",
        "StartHour",
        "EndHour",
        "cID",
        "tID",
        "ClassName",
    ]
)


def generate(
    count, courses, rooms, classes, startDate, endDate, schoolStart=7, schoolEnd=19
):

    dates = generateDates(startDate, endDate)

    df = dfBase.copy()

    startTimer = time.time()

    print(
        f"Generating schedule for {len(dates)} days between {startDate} and {endDate}"
    )
    print(f"Starting at {datetime.fromtimestamp(time.time())}")

    i = 0
    for date in dates:
        dailySchedule = dailyScheduleBase.copy()
        for index, row in classes.iterrows():

            singleClass = row["ClassName"]
            singleClassCourses = row["courses"]

            classSchedule = scheduleClassDay(
                dailySchedule,
                courses,
                singleClass,
                singleClassCourses,
                rooms,
                schoolStart,
                schoolEnd,
            )

            classSchedule["ClassName"] = singleClass
            # print(singleClass)
            dailySchedule = pd.concat([dailySchedule, classSchedule])
        dailySchedule["Date"] = date
        df = pd.concat([df, dailySchedule])
        i += 1

        if i % 10 == 0:
            snapshot = time.time()
            etc = round((snapshot - startTimer) / i * (len(dates) - i))

            timeClass = timedelta(seconds=etc)
            time_string = str(timeClass)
            # print(f"|{startDate}|>>>|{str(date).split(" ")[0]}|>>>|{endDate}|  {round((i * 100)/len(dates),2)}%   ETC:{time_string}s")

    df["Date"] = pd.to_datetime(df["Date"]) + pd.to_timedelta(df["StartHour"], unit="h")
    df.reset_index(inplace=True, drop=True)
    df.reset_index(inplace=True)
    df.rename(columns={"index": "mID"}, inplace=True)

    df = df[["mID", "Date", "RoomNumber", "cID", "ClassName", "StartHour", "EndHour"]]
    return df
