import pandas as pd
import numpy as np
import faker as fk
import os
import random



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
    return np.random.choice(["Male", "Female", "Other"], size=count, p=proportions)


def generateNames(count, genderCol):
    return [
        (
            faker.first_name_male()
            if gender == "Male"
            else (
                faker.first_name_female()
                if gender == "Female"
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


def getKeyByValue(d, value):
    return [k for k, v in d.items() if v == value][0]

def getSchoolYear(date):
    year = int(date.split("-")[0])
    month = int(date.split("-")[1])
    if month < 9:
        return year - 1
    else:
        return year

def fractionRound(x, bin):
    return round(x /bin) * bin

def addTrend(df, seedColumn, trendDict, scoreColumn, minScore, maxScore, resolution):
    df[scoreColumn] = df.apply(lambda x: (fractionRound(x[scoreColumn] + trendDict[x[seedColumn]], resolution)) if x[seedColumn] in trendDict else x[scoreColumn], axis=1)

    df[scoreColumn] = df.apply(lambda x: minScore if x[scoreColumn] < minScore else x[scoreColumn], axis=1)
    df[scoreColumn] = df.apply(lambda x: maxScore if x[scoreColumn] > maxScore else x[scoreColumn], axis=1)



def generatePesel(birthdate, gender):
    year, month, day = str(birthdate.year)[-2:], birthdate.month, birthdate.day

    if birthdate.year >= 2000:
        month += 20

    pesel = f"{year}{month:02d}{day:02d}"

    for _ in range(4):
        pesel += str(random.randint(0, 9))

    if gender == "Male":
        pesel += str(random.choice([1, 3, 5, 7, 9]))
    else:
        pesel += str(random.choice([0, 2, 4, 6, 8]))

    return pesel


def splitDf(df):
    mask = np.random.rand(len(df)) <0.5
    return df[mask], df[~mask]

