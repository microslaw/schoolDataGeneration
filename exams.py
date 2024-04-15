import pandas as pd
import numpy as np
import utils


def generate(count, minScore, maxScore, resolution, df_meetings, df_students, ):

    examMeetings = utils.getLastClassesOfMonth(df_meetings)
    examMeetings = examMeetings[examMeetings["ClassName"] != "Homeroom"]
    df = pd.DataFrame()
    df["sID"] = df_students["sID"]
    df["iq"] = df_students["iq"]
    df["ClassName"] = df_students["ClassName"]
    df["mID"] = df["ClassName"].apply(
        lambda x: [y for y in examMeetings[examMeetings["ClassName"] == x]["mID"]]
    )
    df = df.explode("mID")
    df["Score"] = df["iq"].apply(
        lambda x: min(
            np.random.randint(
                (x / 100) * (minScore / resolution), (x / 100) * (maxScore / resolution)
            )
            * resolution,
            maxScore,
        )
    )

    if count > len(df):
        count = len(df)

    if count > 0:
        df = df.sample(n=count, replace=True)

    df = df.dropna()
    df = df[["sID", "mID", "Score"]]

    return df
