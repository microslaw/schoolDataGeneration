import pandas as pd



def addTrendAdditive(df, seedColumn, trendDict, scoreColumn, minScore, maxScore):
    df[scoreColumn] = df.apply(lambda x: (x[scoreColumn] + trendDict[x[seedColumn]]) if x[seedColumn] in trendDict else x[scoreColumn], axis=1)
    df[scoreColumn] = df.apply(lambda x: minScore if x[scoreColumn] < minScore else x[scoreColumn], axis=1)
    df[scoreColumn] = df.apply(lambda x: maxScore if x[scoreColumn] > maxScore else x[scoreColumn], axis=1)

def addTrendMultiplicative(df, seedColumn, trendDict, scoreColumn, minScore, maxScore):
    df[scoreColumn] = df.apply(lambda x: (x[scoreColumn] * trendDict[x[seedColumn]]) if x[seedColumn] in trendDict else x[scoreColumn], axis=1)
    df[scoreColumn] = df.apply(lambda x: minScore if x[scoreColumn] < minScore else x[scoreColumn], axis=1)
    df[scoreColumn] = df.apply(lambda x: maxScore if x[scoreColumn] > maxScore else x[scoreColumn], axis=1)
