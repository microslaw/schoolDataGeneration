import pandas as pd
import numpy as np
from utils import faker, generateGender, generateNames, generateSurnames, generatePesel
import parameters



def generate(count, minAge, maxAge, cityDistricts, subjects):

    df = pd.DataFrame()
    df.insert(0, 'tID', range(count))
    df["Gender"] = generateGender(count)
    df["Name"] = generateNames(count, df["Gender"])
    df["Surname"] =generateSurnames(count)
    df["CityDistrict"] = np.random.choice(cityDistricts, size=count)
    df["Subject"] = np.random.choice(subjects, size=count)

    df["Birthdate"] = [faker.date_of_birth(minimum_age=minAge, maximum_age=maxAge) for _ in range(count)]

    df["Pesel"] = df.apply(lambda x: generatePesel(birthdate=x["Birthdate"], gender=x["Gender"]), axis=1)

    df = df[["tID", "Name", "Surname", "CityDistrict", "Birthdate", "Gender", "Subject", "Pesel"]]

    return df
