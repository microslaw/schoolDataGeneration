
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


import pandas as pd
import numpy as np

from utils import defaultCityDistricts, defaultCityDistrictsTrendDict, mkdir
import trends

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
"""
May enter infinite loop if:
  - not enough teachers are generated
  - not enough students are generated
  - not enough classrooms are generated
  - too many courses per day need to be scheduled
if that happens restart the kernel, adjust tuple counts, and run the code again
"""


df_classrooms = classroom.generate(357, 999)
df_teachers = teachers.generate(300)
df_courses = course.generate(300, df_teachers)
df_classes, df_courses = aClass.generate(10, df_teachers, df_courses)
df_students = students.generate(800, df_classes)
df_meetings = meeting.generate(0, df_courses, df_classrooms, df_classes, "2022-06-27", "2022-09-5")
df_exams = exams.generate(0, df_meetings, df_students)
df_surveys = surveys.generate(0, df_meetings, df_students, df_courses)
df_attendance = attendance.generate(0, df_meetings, df_students, df_teachers, df_courses)


#This block adds trend: people from different city districts have different scores

df_housing_trend = df_students.copy()
df_housing_trend["score"] = df_housing_trend["CityDistrict"].map(defaultCityDistrictsTrendDict)/50
df_housing_trend = df_housing_trend[["sID", "score"]]
trendDict = { sID: score for sID, score in zip(df_housing_trend["sID"], df_housing_trend["score"]) }
trends.addTrendAdditive(df_surveys, "sID", trendDict , "Score", 0, 20)



#This block loads data from csv files

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



#This block purges unused rows
size =len(df_classrooms)
df_classrooms = df_classrooms[df_classrooms["RoomNumber"].isin(df_meetings["RoomNumber"])]
df_classrooms_removed = df_classrooms[~df_classrooms["RoomNumber"].isin(df_meetings["RoomNumber"])]
print(f"Removed {size - len(df_classrooms)} classrooms")

size =len(df_teachers)
df_teachers = df_teachers[df_teachers["tID"].isin(pd.concat([df_classes["tID"], df_courses["tID"]]).unique())]
df_teachers_removed = df_teachers[~df_teachers["tID"].isin(df_classes["tID"] + df_courses["tID"])]
print(f"Removed {size - len(df_teachers)} teachers")

size =len(df_courses)
df_courses = df_courses[df_courses["cID"].isin(df_classes["courses"].explode().unique())]
df_courses_removed = df_courses[~df_courses["cID"].isin(df_classes["courses"].explode().unique())]
print(f"Removed {size - len(df_courses)} courses")

size =len(df_classes)
df_classes = df_classes[df_classes["ClassName"].isin(df_students["ClassName"])]
df_courses_classes = df_classes[~df_classes["ClassName"].isin(df_students["ClassName"])]
print(f"Removed {size - len(df_classes)} classes")



#This block prepares data for database

path = "data"
headers = False
indexing = False

mkdir(path)

df_students.drop(columns=["iq"]).to_csv(f"{path}/students.csv", index=indexing, header=headers)
df_classes.drop(columns=["Year", "courses"]).to_csv(f"{path}/classes.csv", index=indexing, header=headers)
df_teachers.to_csv(f"{path}/teachers.csv", index=indexing, header=headers)
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


# This block generates updates

path = "updates"

mkdir(path)

df = df_teachers.sample(n=15)
df["CityDistrict2"] = df["CityDistrict"].apply(lambda x: np.random.choice([y for y in defaultCityDistricts if y != x]))
df["update"] = df.apply(lambda x: f"Update Teachers SET CityDistrict = '{x['CityDistrict2']}' WHERE tID = {x['tID']};", axis=1)
df["update"].to_csv(f"{path}/updateTeachersCity.sql", index=False, header=False)

df = df_students.sample(n=15)
df["CityDistrict2"] = df["CityDistrict"].apply(lambda x: np.random.choice([y for y in defaultCityDistricts if y != x]))
df["update"] = df.apply(lambda x: f"Update Students SET CityDistrict = '{x['CityDistrict2']}' WHERE sID = {x['sID']};", axis=1)
df["update"].to_csv(f"{path}/updateStudentsCity.sql", index=False, header=False)

df = df_students.sample(n=15)
df["ClassName2"] = df["ClassName"].apply(lambda x: np.random.choice([y for y in df_classes["ClassName"].unique() if y != x]))
df["update"] = df.apply(lambda x: f"Update Students SET ClassName = '{x['ClassName']}' WHERE sID = {x['sID']};", axis=1)
df["update"].to_csv(f"{path}/updateStudentsClass.sql", index=False, header=False)

df = df_classes.sample(n=15)
df["tID2"] = df["tID"].apply(lambda x: np.random.choice([y for y in df_classes["ClassName"].unique() if y != x]))
df["update"] = df.apply(lambda x: f"Update Class SET tID = '{x['tID']}' WHERE ClassName = '{x['ClassName']}';", axis=1)
df["update"].to_csv(f"{path}/updateClassesTeacher.sql", index=False, header=False)



