import pandas as pd
import numpy as np
import random
import string
from datetime import datetime
from utils import dictToKeyList, defaultSpecializations


def addLetters(specializations):
    letters = string.ascii_uppercase[: len(specializations)]
    random.shuffle(letters)
    return {specializations[i]: letters[i] for i in range(len(specializations))}


def numbersToLetters(numbers):
    return [string.ascii_uppercase[number] for number in numbers]


now = datetime.now()


def generate(
    count,
    teachers,
    courses,
    courseCount=7,
    MaxSchoolYears=6,
    presentYear=now.year - 1 if now.month <= 10 else now.year,
    specializations=defaultSpecializations,
):

    df = pd.DataFrame()
    df.insert(0, "tmpID", range(count * MaxSchoolYears))
    df["Year"] = (df["tmpID"] % MaxSchoolYears)+1
    df["Specialization"] = np.random.choice(dictToKeyList(specializations), count * MaxSchoolYears)
    df["PrefferedCourses"] = df["Specialization"].apply(lambda x: specializations[x])
    df["ClassName"] = numbersToLetters(df["tmpID"] // MaxSchoolYears)
    df["ClassName"] = df["ClassName"] + (presentYear - df["Year"]).astype(str).apply(
        lambda x: x[2:]
    )
    df["tID"] = np.random.choice(teachers["tID"], count * MaxSchoolYears)
    # df.insert(0, "courses", [])



    df_homeroom_courses = pd.DataFrame()
    df_homeroom_courses.insert(0, "cID", range(len(courses), len(courses) + len(df)))
    df_homeroom_courses["Name"] = "Homeroom"
    df_homeroom_courses["Year"] = df["Year"]
    df_homeroom_courses["tID"] = df["tID"]
    df_homeroom_courses["ClassName"] = df["ClassName"]

    def getRandomCourses(specialization, courses, courseCount, year):
        prefferedCourses = courses[courses["Name"].isin(specializations[specialization])]
        chosenPrefferedCourses = [x for x in np.random.choice(prefferedCourses["cID"], size=(courseCount//2))]
        chosenNormalCourses = [x for x in np.random.choice(courses["cID"], size=min(courseCount - (courseCount//2),len(courses)), replace=False)]
        return chosenPrefferedCourses + chosenNormalCourses

    for year in courses["Year"].unique():
        appropriateCourses = courses[courses["Year"] == year]
        df.loc[df["Year"] == year, "courses"] = df["Specialization"].apply(
            getRandomCourses, args=(appropriateCourses, courseCount, year)
        )

    df["homeroomCourse"] = [
        [
            df_homeroom_courses[df_homeroom_courses["ClassName"] == row["ClassName"]][
                "cID"
            ].values[0]
        ]
        for index, row in df.iterrows()
    ]

    df["courses"] = df["courses"] + df["homeroomCourse"]

    df_homeroom_courses = df_homeroom_courses[["cID", "Name", "Year", "tID"]]

    df_all_courses = pd.concat([courses, df_homeroom_courses])
    df = df[["ClassName", "Year", "Specialization", "tID", "courses"]]

    return df, df_all_courses
