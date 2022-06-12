import pandas as pd


# return a dictionary of authority objects username:twid (key:value)
def getTop25():
    df =pd.read_csv("./database/top25.csv",
                    lineterminator='\n', index_col=0)
    return df
