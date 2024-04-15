import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np

from utils import mkdir, getSchoolYear, addTrend
import parameters

import classroom
import teachers
import course
import aClass
import students
import meeting
import exams
import surveys
import attendance


# This block generates data

df_classrooms = classroom.generate(
    count=parameters.classroom_count,
    maxRoomNumber=parameters.classroom_max_number,
    MinMaxCapacity=parameters.classroom_min_max_capacity,
    MaxMaxCapacity=parameters.classroom_max_max_capacity,
)

df_teachers = teachers.generate(
    count=parameters.teacher_count,
    minAge=parameters.teacher_min_age,
    maxAge=parameters.teacher_max_age,
    cityDistricts=parameters.default_city_districts,
    subjects=parameters.default_course_names,
)

df_courses = course.generate(
    count=parameters.course_count,
    maxSchoolYears=parameters.max_school_years,
    courseNames=parameters.default_course_names,
    df_teachers=df_teachers,
)

df_classes, df_courses = aClass.generate(
    count=parameters.class_count,
    courseCount=parameters.course_count,
    maxSchoolYears=parameters.max_school_years,
    presentYear=getSchoolYear(parameters.start_date),
    specializations=parameters.default_specializations,
    df_teachers=df_teachers,
    df_courses=df_courses,
)

df_students = students.generate(
    count=parameters.student_count,
    minAge=parameters.student_min_age,
    cityDistricts=parameters.default_city_districts,
    classes=df_classes,
)


df_meetings = meeting.generate(
    count=parameters.meeting_count,
    startDate=parameters.start_date,
    endDate=parameters.end_date,
    schoolStart=parameters.school_start_hour,
    schoolEnd=parameters.school_end_hour,
    maxSchoolYears=parameters.max_school_years,
    df_courses=df_courses,
    df_rooms=df_classrooms,
    df_classes=df_classes,
)

df_exams = exams.generate(
    count=parameters.exam_count,
    minScore=parameters.exam_min_score,
    maxScore=parameters.exam_max_score,
    resolution=parameters.exam_resolution,
    df_meetings=df_meetings,
    df_students=df_students,
)

df_surveys = surveys.generate(
    count=parameters.survey_count,
    minScore=parameters.survey_min_score,
    maxScore=parameters.survey_max_score,
    resolution=parameters.survey_resolution,
    df_meetings=df_meetings,
    df_students=df_students,
    df_courses=df_courses,
)

df_attendance = attendance.generate(
    count=parameters.attendance_count,
    excusedProb=parameters.excused_prob,
    lateProb=parameters.late_prob,
    attendanceProb=parameters.attendance_prob,
    df_meetings=df_meetings,
    df_students=df_students,
    df_teachers=df_teachers,
    df_courses=df_courses,
    catchupTasks=parameters.default_catchup_tasks,
)




#This block purges unused rows
size =len(df_classrooms)
df_classrooms = df_classrooms[df_classrooms["RoomNumber"].isin(df_meetings["RoomNumber"])]
df_classrooms_removed = df_classrooms[~df_classrooms["RoomNumber"].isin(df_meetings["RoomNumber"])]
print(f"Removed {size - len(df_classrooms)} unused classrooms")

size =len(df_teachers)
df_teachers = df_teachers[df_teachers["tID"].isin(pd.concat([df_classes["tID"], df_courses["tID"]]).unique())]
df_teachers_removed = df_teachers[~df_teachers["tID"].isin(df_classes["tID"] + df_courses["tID"])]
print(f"Removed {size - len(df_teachers)} unused teachers")

size =len(df_courses)
df_courses = df_courses[df_courses["cID"].isin(df_classes["courses"].explode().unique())]
df_courses_removed = df_courses[~df_courses["cID"].isin(df_classes["courses"].explode().unique())]
print(f"Removed {size - len(df_courses)} unused courses")

size =len(df_classes)
df_classes = df_classes[df_classes["ClassName"].isin(df_students["ClassName"])]
df_courses_classes = df_classes[~df_classes["ClassName"].isin(df_students["ClassName"])]
print(f"Removed {size - len(df_classes)} unused classes")




#This block adds trend: people from different city districts have different scores

df_housing_trend = df_students.copy()
df_housing_trend["score"] = df_housing_trend["CityDistrict"].map(parameters.default_city_districts_trend_dict)/50
df_housing_trend = df_housing_trend[["sID", "score"]]
trendDict = { sID: score for sID, score in zip(df_housing_trend["sID"], df_housing_trend["score"]) }
addTrend(df_surveys, "sID", trendDict , "Score", 0, 20, parameters.survey_resolution)




#This block adds trend: teachers influence the scores of their students

teacherTrendDict = {tID: score for tID, score in zip(df_teachers["tID"], np.random.uniform(-2, 5, len(df_teachers)))}
df_meeting_teachers = df_meetings.merge(df_courses, left_on="cID", right_on="cID", how="left")[["mID", "tID"]]
trendDict = { mID: teacherTrendDict[tID] for mID,tID in df_meeting_teachers.values}
addTrend(df_exams, "mID", trendDict, "Score", 0, 50, parameters.exam_resolution)




#This block adds trend: room where the exam was taken influences the score

roomTrendDict = {roomNumber: score for roomNumber, score in zip(df_classrooms["RoomNumber"], np.random.uniform(-5, 5, len(df_classrooms)))}
df_meeting_rooms = df_meetings[["mID", "RoomNumber"]]
trendDict = { mID: roomTrendDict[rID] for mID,rID in df_meeting_rooms.values}
addTrend(df_exams, "mID", trendDict, "Score", 0, 50, parameters.exam_resolution)




#This saves data to .csv files, in format compatible with the database

path = "data"
headers = False
indexing = False

mkdir(path)

df_students.drop(columns=["iq"]).to_csv(f"{path}/students.csv", index=indexing, header=headers)
df_classes.drop(columns=["Year", "courses"]).to_csv(f"{path}/classes.csv", index=indexing, header=headers)
df_teachers.drop(columns=["Subject"]).to_csv(f"{path}/teachers.csv", index=indexing, header=headers)
df_courses.to_csv(f"{path}/courses.csv", index=indexing, header=headers)
df_classrooms.to_csv(f"{path}/classrooms.csv", index=indexing, header=headers)
df_meetings.drop(columns=["StartHour", "EndHour", "Year", "Month"]).to_csv(f"{path}/meetings.csv", index=indexing, header=headers)
df_surveys.to_csv(f"{path}/surveys.csv", index=indexing, header=headers)
df_exams.to_csv(f"{path}/exams.csv", index=indexing, header=headers)
df_attendance.to_csv(f"{path}/attendance.csv", index=indexing, header=headers)




#This block prepares data for backup, in format not suitable for database

path = "backup"
headers = True
indexing = False

mkdir(path)

df_students.to_csv(f"{path}/students.csv", index=indexing, header=headers)
df_classes.to_csv(f"{path}/classes.csv", index=indexing, header=headers)
df_teachers.to_csv(f"{path}/teachers.csv", index=indexing, header=headers)
df_courses.to_csv(f"{path}/courses.csv", index=indexing, header=headers)
df_classrooms.to_csv(f"{path}/classrooms.csv", index=indexing, header=headers)
df_meetings.to_csv(f"{path}/meetings.csv", index=indexing, header=headers)
df_surveys.to_csv(f"{path}/surveys.csv", index=indexing, header=headers)
df_exams.to_csv(f"{path}/exams.csv", index=indexing, header=headers)
df_attendance.to_csv(f"{path}/attendance.csv", index=indexing, header=headers)




#This block loads data from csv files.

path = "data"

df_classrooms = pd.read_csv(f"{path}/classrooms.csv")
df_teachers = pd.read_csv(f"{path}/teachers.csv")
df_courses = pd.read_csv(f"{path}/courses.csv")
df_classes = pd.read_csv(f"{path}/classes.csv")
df_students = pd.read_csv(f"{path}/students.csv")
df_meetings = pd.read_csv(f"{path}/meetings.csv")
df_exams = pd.read_csv(f"{path}/exams.csv")
df_surveys = pd.read_csv(f"{path}/surveys.csv")
df_attendance = pd.read_csv(f"{path}/attendance.csv")



