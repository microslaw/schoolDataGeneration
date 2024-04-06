import pandas as pd
import numpy as np
import utils


def generate(count, meetings, students, minScore=0, maxScore=50, resolution=1 / 4):

    examMeetings = utils.getLastClassesOfMonth(meetings)
    examMeetings = examMeetings[examMeetings["ClassName"] != "Homeroom"]
    df = pd.DataFrame()
    df["sID"] = students["sID"]
    df["iq"] = students["iq"]
    df["ClassName"] = students["ClassName"]
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

    df = df[["sID", "mID", "Score"]]

    return df
