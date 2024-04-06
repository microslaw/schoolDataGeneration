import pandas as pd
import numpy as np
from utils import defaultCityDistricts, faker, generateGender, generateNames, generateSurnames


def generate(count, minAge=25, maxAge=65, cityDistricts = defaultCityDistricts):

    df = pd.DataFrame()
    df.insert(0, 'tID', range(count))
    df["Gender"] = generateGender(count)
    df["Name"] = generateNames(count, df["Gender"])
    df["Surname"] =generateSurnames(count)
    df["CityDistrict"] = np.random.choice(cityDistricts, size=count)

    df["Birthdate"] = [faker.date_of_birth(minimum_age=minAge, maximum_age=maxAge) for _ in range(count)]

    df = df[["tID", "Name", "Surname", "CityDistrict", "Birthdate", "Gender"]]

    return df
