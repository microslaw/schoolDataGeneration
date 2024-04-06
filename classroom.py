import pandas as pd
import numpy as np



def generate(count, maxRoomNumber, floors = 8, MinMaxCapacity = 15, MaxMaxCapacity = 40):

    df = pd.DataFrame()
    df["RoomNumber"] = np.random.choice(range(1, maxRoomNumber), size=count, replace=False)
    df.sort_values("RoomNumber", inplace=True)
    df.reset_index(inplace=True, drop=True)
    df.reset_index(inplace=True)
    floorRooms = count // floors
    df["Floor"] = df["index"] // floorRooms
    df["MaxCapacity"] = np.random.randint(MinMaxCapacity, MaxMaxCapacity, size=count)

    df = df[["RoomNumber", "Floor", "MaxCapacity"]]

    return df
