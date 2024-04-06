import pandas as pd
import numpy as np
import faker as fk
import utils


def generate(count, meetings,  students, courses, minScore=0, maxScore=20, resolution=1/4):

    lastMeetings = utils.getLastClassesOfMonth(meetings)
    homeRoomCourses = courses[courses["Name"] == "Homeroom"]
    surveyMeetings = lastMeetings[lastMeetings["cID"].isin(homeRoomCourses["cID"])]
    df = pd.DataFrame()
    df["sID"] = students["sID"]
    df["ClassName"] = students["ClassName"]
    df["mID"] = df["ClassName"].apply(lambda x: [y for y in surveyMeetings[surveyMeetings["ClassName"] == x]["mID"]])
    df = df.explode("mID")
    df["Score"] = np.random.randint(minScore/resolution, maxScore/resolution, size=len(df))*resolution


    df = df[["mID", "sID", "Score"]]

    return df
