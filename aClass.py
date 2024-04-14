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
    df["Year"] = (df["tmpID"] % MaxSchoolYears) + 1
    df["Specialization"] = np.random.choice(
        dictToKeyList(specializations), count * MaxSchoolYears
    )
    df["ClassName"] = numbersToLetters(df["tmpID"] // MaxSchoolYears)
    df["ClassName"] = df["ClassName"] + (presentYear - df["Year"]).astype(str).apply(
        lambda x: x[2:]
    )
    df["tID"] = np.random.choice(teachers["tID"], count * MaxSchoolYears)
    # df.insert(0, "courses", [])

    df_homeroom_courses = pd.DataFrame()

    id_start = len(courses)
    for year in range(0, MaxSchoolYears):

        df_yearly_homeroom_courses = pd.DataFrame()
        df_yearly_homeroom_courses.insert(0, "cID", range(id_start, id_start + len(df)))
        id_start += len(df)
        df_yearly_homeroom_courses["Name"] = "Homeroom"
        df_yearly_homeroom_courses["Year"] = df["Year"] + year
        df_yearly_homeroom_courses["tID"] = df["tID"]
        df_yearly_homeroom_courses["ClassName"] = df["ClassName"]
        df_homeroom_courses = pd.concat(
            [df_homeroom_courses, df_yearly_homeroom_courses]
        )

    def getRandomCourses(specialization, courses, courseCount, year):
        chosenPrefferedCourses = []
        chosenNormalCourses = []

        for course_year in range(year, MaxSchoolYears + 1):
            age_matching_courses = courses[courses["Year"] == course_year]
            prefferedCourses = age_matching_courses[
                age_matching_courses["Name"].isin(specializations[specialization])
            ]
            prefferedCourses = [
                x
                for x in np.random.choice(prefferedCourses["cID"], size=(courseCount // 2))
            ]

            normalCourses = [
                x
                for x in np.random.choice(
                    age_matching_courses["cID"],
                    size=min(courseCount - (courseCount // 2), len(age_matching_courses)),
                    replace=False,
                )
            ]
            chosenPrefferedCourses.extend(prefferedCourses)
            chosenNormalCourses.extend(normalCourses)
        return chosenPrefferedCourses + chosenNormalCourses

    for year in courses["Year"].unique():
        df.loc[df["Year"] == year, "courses"] = df["Specialization"].apply(
            getRandomCourses, args=(courses, courseCount, year)
        )

    df["homeroomCourses"] = [
        [
            df_homeroom_courses[df_homeroom_courses["ClassName"] == row["ClassName"]][
                "cID"
            ]
        ]
        for index, row in df.iterrows()
    ]

    df["homeroomCourses"] = [x[0].values for x in df["homeroomCourses"]]

    for index, row in df.iterrows():
        row["courses"].extend(row["homeroomCourses"])

    # df["courses"] = df["homeroomCourses"]

    df_homeroom_courses = df_homeroom_courses[["cID", "Name", "Year", "tID"]]

    df_all_courses = pd.concat([courses, df_homeroom_courses])
    df = df[["ClassName", "Year", "Specialization", "tID", "courses"]]

    return df, df_all_courses
