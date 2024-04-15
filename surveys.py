import pandas as pd
import numpy as np
import faker as fk
import utils


def generate(count, minScore, maxScore, resolution, df_meetings,  df_students, df_courses,):

    lastMeetings = utils.getLastClassesOfMonth(df_meetings)
    homeRoomCourses = df_courses[df_courses["Name"] == "Homeroom"]
    surveyMeetings = lastMeetings[lastMeetings["cID"].isin(homeRoomCourses["cID"])]
    df = pd.DataFrame()
    df["sID"] = df_students["sID"]
    df["ClassName"] = df_students["ClassName"]
    df["mID"] = df["ClassName"].apply(lambda x: [y for y in surveyMeetings[surveyMeetings["ClassName"] == x]["mID"]])
    df = df.explode("mID")
    df["Score"] = np.random.randint(minScore/resolution, maxScore/resolution, size=len(df))*resolution


    df = df[["mID", "sID", "Score"]]
    df = df.dropna()

    if count > len(df):
        count = len(df)

    if count > 0:
        df = df.sample(n=count, replace=True)

    return df
