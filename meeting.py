import pandas as pd
import numpy as np
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
    freeTeachersList = list(freeTeachersSet.intersection(teachersNeeded))
    random.shuffle(freeTeachersList)
    freeTeachersSet = set(freeTeachersList)

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



def scheduleClassDay(df, teachersDict, roomsDict, schoolStart, schoolEnd, classCoursesTeachersDict):
    schedule = pd.DataFrame(
        columns=["RoomNumber", "StartHour", "EndHour", "cID", "tID"]
    )
    for hour in range(schoolStart, schoolEnd):

        room = getFreeRoom(roomsDict, hour)
        teacher = getFreeTeacher(teachersDict, hour, classCoursesTeachersDict.values())
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
                teachersDict[hour].add(teacher)
            if teacher is None:
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
    count,startDate, endDate, schoolStart, schoolEnd, maxSchoolYears,  df_courses, df_rooms, df_classes,
):

    dates = generateDates(startDate, endDate)

    df = dfBase.copy()


    print(
        f"Generating schedule for {len(dates)} days between {startDate} and {endDate}"
    )
    print(f"Starting at {str(datetime.fromtimestamp(time.time())).split(".")[0]}\n")

    i = 1
    courseYearDict = {year: {cID for cID in df_courses[df_courses["Year"] == year]["cID"]} for year in df_courses["Year"].unique()}
    for non_existing_year in range(maxSchoolYears * 2):
        if non_existing_year not in courseYearDict:
            courseYearDict[non_existing_year] = {}

    year = 1
    present_classes = df_classes.copy()
    present_classes["courses"] = present_classes.apply(lambda row: {cID for cID in row["courses"] if cID in courseYearDict[year + row["Year"]]}, axis=1)
    prevDate = dates.iloc[0]

    startTimer = time.time()
    for date in dates:
        try:
            #if date is the last day before summer break, change the year
            if date.month == 9 and prevDate.month == 6:
                year += 1
                present_classes = df_classes.copy()
                present_classes["courses"] = present_classes.apply(lambda row: {cID for cID in row["courses"] if cID in courseYearDict[year + row["Year"]]}, axis=1)


            prevDate = date
            dailySchedule = dailyScheduleBase.copy()
            teachersSchedule = getAllTeachersCombinations(df_courses["tID"].unique(), schoolStart, schoolEnd)
            roomsSchedule = getAllRoomsCombinations(df_rooms["RoomNumber"].unique(), schoolStart, schoolEnd)



            for index, row in present_classes.iterrows():

                singleClass = row["ClassName"]
                singleClassCourses = row["courses"]
                singleClassCourses = {cID : tID for cID, tID in df_courses[["cID", "tID"]].values if cID in singleClassCourses}

                classSchedule = scheduleClassDay(
                    dailySchedule,
                    teachersSchedule,
                    roomsSchedule,
                    schoolStart,
                    schoolEnd,
                    singleClassCourses,
                )

                classSchedule["ClassName"] = singleClass
                dailySchedule = pd.concat([dailySchedule, classSchedule])
        except Exception as e:
            with open("error_log.txt", "a") as f:
                f.write(f"Error at {str(date)}: {str(e)}\n")
        finally:
            pass

        dailySchedule["Date"] = date
        df = pd.concat([df, dailySchedule])

        snapshot = time.time()
        etc = round((snapshot - startTimer) / i * (len(dates) - i))
        timeClass = timedelta(seconds=etc)
        time_string = str(timeClass)
        toPrint = f"|{startDate}|>>>|{str(date).split(" ")[0]}|>>>|{endDate}|"
        toPrint += f"{str(round((i * 100)/len(dates),2)).ljust(3, '0')}%   ETC:{time_string}s   "
        print(toPrint, end="\r")
        i += 1

    print("\n")
    print(f"Finished at {str(datetime.fromtimestamp(time.time())).split(".")[0]}\n")


    df["Date"] = pd.to_datetime(df["Date"]) + pd.to_timedelta(df["StartHour"], unit="h")
    df.reset_index(inplace=True, drop=True)
    df.reset_index(inplace=True)
    df["MeetingDurationMinutes"] = np.random.randint(10, 60)
    df.rename(columns={"index": "mID"}, inplace=True)

    df = df[["mID", "Date", "RoomNumber", "cID", "ClassName", "StartHour", "EndHour", "MeetingDurationMinutes"]]

    if count > len(df):
        count = len(df)

    if count > 0:
        df = df.sample(n=count, replace=True)


    return df
