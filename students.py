import pandas as pd
import numpy as np
from utils import faker, generateGender, generateNames, generateSurnames, generatePesel


def generate(count, classes, minAge, cityDistricts):
    df = pd.DataFrame()
    df.insert(0, "sID", range(count))
    df["Gender"] = generateGender(count)
    df["Name"] = generateNames(count, df["Gender"])
    df["Surname"] =generateSurnames(count)
    df["CityDistrict"] = np.random.choice(cityDistricts,size=count)
    df["Year"] = np.random.choice(classes["Year"].unique(), size=count)
    df["Birthdate"] = df["Year"].apply(
        lambda x: faker.date_of_birth(
            minimum_age=x + minAge, maximum_age=minAge + x + 1
        )
    )
    df["ClassName"] = df["Year"].apply(
        lambda x: np.random.choice(classes[classes["Year"] == x]["ClassName"])
    )
    df["iq"] = np.random.randint(70, 130, size=count)

    df["Pesel"] = df.apply(lambda x: generatePesel(birthdate=x["Birthdate"], gender=x["Gender"]), axis=1)


    df = df[["sID", "Name", "Surname", "CityDistrict", "Birthdate", "Gender", "ClassName", "iq", "Pesel"]]

    return df
