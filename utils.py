import pandas as pd
import numpy as np
import faker as fk
import os

defaultCityDistricts = [
    "Wejherowo",
    "Redlowo",
    "Orlowo",
    "Reda",
    "Gdynia centrum",
    "Gdansk centrum",
    "Zaspa",
    "Jasien",
    "Orunia",
    "Przymorze",
    "Wrzeszcz",
    "Stocznia",
    "Lostowice",
]


defaultCityDistrictsTrendDict = {

    "Wejherowo" : 70,
    "Redlowo" : 40,
    "Orlowo" :35,
    "Reda" :55,
    "Gdynia centrum": 50,
    "Gdansk centrum": 20,
    "Zaspa" : 20,
    "Jasien" : 40,
    "Orunia" : 30,
    "Przymorze" : 25,
    "Wrzeszcz" : 15,
    "Stocznia" : 10,
    "Lostowice" : 60,
}



defaultSpecializations = {
    "Mathematical": ["Mathematics", "Physics", "Informatics"],
    "Humanistic": ["Polish", "Psychology", "History"],
    "Scientific": ["Biology", "Chemistry", "Physics"],
    "Linguistic": ["English", "German", "French"],
    "Artistic": ["Art", "Music", "History"],
    "Sport": ["PE", "Biology", "Physics"],
}


defaultCourseNames = [
    "Mathematics",
    "Polish",
    "English",
    "Physics",
    "Chemistry",
    "Biology",
    "History",
    "Geography",
    "PE",
    "Art",
    "Music",
    "Informatics",
    "Religion",
    "Ethics",
    "Psychology",
    "Sociology",
    "Philosophy",
    "Economics",
    "German",
    "French"
]

#specialization/course check
for key,value in defaultSpecializations.items():
    for course in value:
        if course not in defaultCourseNames:
            raise ValueError(f"Course {course} is not in defaultCourseNames")


faker = fk.Faker()





def generateDates(start, end):
    dates = pd.DataFrame()
    dates["dates"] = pd.date_range(start=start, end=end)
    dates = dates[dates["dates"].dt.dayofweek < 5]
    dates = dates[~dates["dates"].dt.month.isin([7, 8])]

    return dates["dates"]


def getLastClassesOfMonth(df):

    # df["Date"] = pd.to_datetime(df["Date"])
    df["Date"] = df["Date"].apply(lambda x: str(x))
    df["Year"] = df["Date"].apply(lambda x: x.split("-")[0])
    df["Month"] = df["Date"].apply(lambda x: x.split("-")[1])
    df = df[
        df["Date"]
        == df.groupby(["Year", "Month", "cID", "ClassName"])["Date"].transform("max")
    ]

    return df


def dictToKeyList(d):
    return [k for k, _ in d.items()]


def generateGender(count, proportions=[0.45, 0.45, 0.1]):
    return np.random.choice(["M", "F", "O"], size=count, p=proportions)


def generateNames(count, genderCol):
    return [
        (
            faker.first_name_male()
            if gender == "M"
            else (
                faker.first_name_female()
                if gender == "F"
                else faker.first_name_nonbinary()
            )
        )
        for gender in genderCol
    ]

def generateSurnames(count):
    return [faker.last_name() for _ in range(count)]

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
    print(f"Directory {path} already exists")
