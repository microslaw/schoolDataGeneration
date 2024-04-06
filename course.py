import pandas as pd
import numpy as np
from utils import defaultCourseNames


def generate(count, teachers_df, MaxSchoolYears=6, courseNames=defaultCourseNames):

    df = pd.DataFrame()
    df.insert(0, "cID", range(count))
    df["Name"] = np.random.choice(courseNames, size=count)
    df["Year"] = np.random.randint(1, MaxSchoolYears+1, size=count)
    df["tID"] = np.random.choice(teachers_df["tID"], size=count)

    df = df[["cID", "Name", "Year", "tID"]]

    return df
