import pandas as pd
import random
import time
from datetime import timedelta, datetime
from utils import generateDates, getKeyByValue
from timer import *


def isRoomFree(df, room, startHour, endHour):
    df = df[df["RoomNumber"] == room]
    df = df[df["EndHour"] > startHour]
    df = df[df["StartHour"] < endHour]

    if len(df) > 0:
        return False
    return True


def getAllRoomsCombinations(rooms, schoolStart, schoolEnd):
    rooms = list(rooms)
    freeRooms = {hour: rooms.copy() for hour in range(schoolStart, schoolEnd + 1)}
    for hour, rooms in freeRooms.items():
        random.shuffle(rooms)
        freeRooms[hour] = rooms
    return freeRooms

def getFreeRoom(freeRooms, startHour):
    freeRoomsList = freeRooms[startHour]
    if len(freeRoomsList) > 0:
        return freeRoomsList.pop()
    return None

def getAllTeachersCombinations(teachers, schoolStart, schoolEnd):
    freeTeachers = {hour: teachers.copy() for hour in range(schoolStart, schoolEnd + 1)}
    for hour, teachers in freeTeachers.items():
        random.shuffle(teachers)
        freeTeachers[hour] = set(teachers)
    return freeTeachers

def getFreeTeacher(freeTeachers, startHour, teachersNeeded):
    freeTeachersSet = freeTeachers[startHour]
    freeTeachersSet = freeTeachersSet.intersection(teachersNeeded)
    if len(freeTeachersSet) > 0:
        toReturn = freeTeachersSet.pop()
        freeTeachers[startHour].remove(toReturn)
        return toReturn
    return None



def isTeacherFree(df, tID, startHour, endHour):
    df = df[df["tID"] == tID]
    df = df[df["EndHour"] > startHour]
    df = df[df["StartHour"] < endHour]

    if len(df) > 0:
        return False
    return True


# def scheduleClassDay(df, courses, aClass, aClassCourses, rooms, schoolStart, schoolEnd):
#     """
#     aClass is id of a class that has schedule made for them
#     aClassCourses is a list of courses that the class has
#     courses is a dataframe with all courses
#     """

#     schedule = pd.DataFrame(
#         columns=["RoomNumber", "StartHour", "EndHour", "cID", "tID"]
#     )
#     start = schoolStart
#     rooms = list(rooms["RoomNumber"].unique())
#     freeRooms = getAllRoomsCombinations(rooms, schoolStart, schoolEnd)

#     teachersCourses = [row for index, row in courses[["cID", "tID"]].iterrows()]
#     freeTeachers = getAllTeachersCombinations(teachersCourses, schoolStart, schoolEnd)
#     courses = courses[courses["cID"].isin(aClassCourses)]
#     for index, row in courses[["cID", "tID"]].iterrows():
#         if (
#             isClassFree(df, aClass, start, start + 1)
#             and isTeacherFree(df, row["tID"], start, start + 1)
#         ):
#             room = getFreeRoom(freeRooms, start)

#             schedule.loc[len(schedule) + len(df)] = {
#                 "RoomNumber": room,
#                 "StartHour": start,
#                 "EndHour": start + 1,
#                 "cID": row["cID"],
#                 "tID": row["tID"],
#             }
#             break
#         else:
#             start += 1
#     return schedule

def scheduleClassDay(df, teachersDict, roomsDict, schoolStart, schoolEnd, classCoursesTeachersDict):
    schedule = pd.DataFrame(
        columns=["RoomNumber", "StartHour", "EndHour", "cID", "tID"]
    )
    for hour in range(schoolStart, schoolEnd):
        # for key, value in roomsDict.items():
        #     print(key, value)
        # input()
        timer_schedulers.tic()
        room = getFreeRoom(roomsDict, hour)
        teacher = getFreeTeacher(teachersDict, hour, classCoursesTeachersDict.values())
        timer_schedulers.toc()
        if room is not None and teacher is not None:
            cID = getKeyByValue(classCoursesTeachersDict, teacher)
            schedule.loc[len(schedule) + len(df)] = {
                "RoomNumber": room,
                "StartHour": hour,
                "EndHour": hour + 1,
                "cID": cID,
                "tID": teacher,
            }

            classCoursesTeachersDict.pop(cID)
            if classCoursesTeachersDict == {}:
                break
        else:
            if room is None:
                # print("No room available")
                teachersDict[hour].append(teacher)
            if teacher is None:
                # print("No teacher available")
                roomsDict[hour].append(room)

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

    i = 1
    for date in dates:
        timer_combinations.tic()
        dailySchedule = dailyScheduleBase.copy()
        teachersSchedule = getAllTeachersCombinations(courses["tID"].unique(), schoolStart, schoolEnd)
        roomsSchedule = getAllRoomsCombinations(rooms["RoomNumber"].unique(), schoolStart, schoolEnd)
        timer_combinations.toc()

        timer_all_classes.tic()

        classes

        for index, row in classes.iterrows():

            singleClass = row["ClassName"]
            singleClassCourses = row["courses"]
            singleClassCourses = {cID : tID for cID, tID in courses[["cID", "tID"]].values if cID in singleClassCourses}

            timer_schedule_class_day.tic()
            classSchedule = scheduleClassDay(
                dailySchedule,
                teachersSchedule,
                roomsSchedule,
                schoolStart,
                schoolEnd,
                singleClassCourses,
            )
            timer_schedule_class_day.toc()

            classSchedule["ClassName"] = singleClass
            dailySchedule = pd.concat([dailySchedule, classSchedule])
        dailySchedule["Date"] = date
        df = pd.concat([df, dailySchedule])

        snapshot = time.time()
        etc = round((snapshot - startTimer) / i * (len(dates) - i))
        timeClass = timedelta(seconds=etc)
        time_string = str(timeClass)
        print(f"|{startDate}|>>>|{str(date).split(" ")[0]}|>>>|{endDate}|", end="")
        print(f"{str(round((i * 100)/len(dates),2)).ljust(3, '0')}%   ETC:{time_string}s")
        i += 1
        timer_all_classes.toc()

    df["Date"] = pd.to_datetime(df["Date"]) + pd.to_timedelta(df["StartHour"], unit="h")
    df.reset_index(inplace=True, drop=True)
    df.reset_index(inplace=True)
    df.rename(columns={"index": "mID"}, inplace=True)

    df = df[["mID", "Date", "RoomNumber", "cID", "ClassName", "StartHour", "EndHour"]]

    print("\nTimer schedule class day:")
    timer_schedule_class_day.stats()
    timer_schedule_class_day.reset()

    print("\nTimer all classes:")
    timer_all_classes.stats()
    timer_all_classes.reset()

    print("\nTimer combinations:")
    timer_combinations.stats()
    timer_combinations.reset()

    print("\nTimer schedulers:")
    timer_schedulers.stats()
    timer_schedulers.reset()

    return df
