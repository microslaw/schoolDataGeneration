import pandas as pd
import numpy as np


def generate(count, df_teachers, maxSchoolYears, courseNames):

    df = pd.DataFrame()
    df.insert(0, "cID", range(count))
    df["Year"] = np.random.randint(1, maxSchoolYears+1, size=count)
    df["tID"] = np.random.choice(df_teachers["tID"], size=count)
    df["Name"] = df["tID"].map(df_teachers.set_index("tID")["Subject"])
    df = df[["cID", "Name", "Year", "tID"]]

    return df
