import pandas as pd
import numpy as np

file_location = input("Input File Location: ")

df = pd.read_csv(r"" + file_location)

for x in df.index:
    One_Phone = df.iloc[x]["Owner 1 Phone Numbers"]
    Two_Phone = df.iloc[x]["Owner 2 Phone Numbers"]
    New_One_Phone = []
    New_Two_Phone = []

    if type(One_Phone) == str:
        One_Phone = One_Phone.split(", ")
        for i in range(len(One_Phone)):
            if "DNC" not in One_Phone[i]:
                New_One_Phone.append(One_Phone[i])
    df.at[x, "Owner 1 Phone Numbers"] = New_One_Phone

    if type(Two_Phone) == str:
        Two_Phone = Two_Phone.split(", ")
        for i in range(len(Two_Phone)):
            if "DNC" not in Two_Phone[i]:
                New_Two_Phone.append(Two_Phone[i])
    df.at[x, "Owner 2 Phone Numbers"] = New_Two_Phone

df2 = pd.DataFrame().reindex_like(df)

rows = 0

for x in df.index:
    Address = df.iloc[x]["Property Address"]
    City = df.iloc[x]["City"]
    State = df.iloc[x]["State"]
    Zip = df.iloc[x]["ZIP 5"]
    One_First = df.iloc[x]["Owner 1 First Name"]
    One_Last = df.iloc[x]["Owner 1 Last Name"]
    One_Phone = df.at[x, "Owner 1 Phone Numbers"]
    Two_First = df.iloc[x]["Owner 2 First Name"]
    Two_Last = df.iloc[x]["Owner 2 Last Name"]
    Two_Phone = df.at[x, "Owner 2 Phone Numbers"]

    if len(df.at[x, "Owner 1 Phone Numbers"]) or len(df.at[x, "Owner 2 Phone Numbers"]) > 0:
        for i in range(0, max(len(One_Phone), len(Two_Phone))):
            df2.at[x + rows, "Property Address"] = Address
            df2.at[x + rows, "City"] = City
            df2.at[x + rows, "State"] = State
            df2.at[x + rows, "ZIP 5"] = Zip
            if i < len(One_Phone):
                df2.at[x + rows, "Owner 1 First Name"] = One_First
                df2.at[x + rows, "Owner 1 Last Name"] = One_Last
                df2.at[x + rows, "Owner 1 Phone Numbers"] = One_Phone[i]
            elif i == 0:
                df2.at[x + rows, "Owner 1 First Name"] = One_First
                df2.at[x + rows, "Owner 1 Last Name"] = One_Last
                df2.at[x + rows, "Owner 1 Phone Numbers"] = np.nan
            else:
                df2.at[x + rows, "Owner 1 First Name"] = np.nan
                df2.at[x + rows, "Owner 1 Last Name"] = np.nan
                df2.at[x + rows, "Owner 1 Phone Numbers"] = np.nan
            if i < len(Two_Phone):
                df2.at[x + rows, "Owner 2 First Name"] = Two_First
                df2.at[x + rows, "Owner 2 Last Name"] = Two_Last
                df2.at[x + rows, "Owner 2 Phone Numbers"] = Two_Phone[i]
            elif i == 0:
                df2.at[x + rows, "Owner 2 First Name"] = Two_First
                df2.at[x + rows, "Owner 2 Last Name"] = Two_Last
                df2.at[x + rows, "Owner 2 Phone Numbers"] = np.nan
            else:
                df2.at[x + rows, "Owner 2 First Name"] = np.nan
                df2.at[x + rows, "Owner 2 Last Name"] = np.nan
                df2.at[x + rows, "Owner 2 Phone Numbers"] = np.nan
            rows += 1
    else:
        df2.at[x + rows, "Property Address"] = Address
        df2.at[x + rows, "City"] = City
        df2.at[x + rows, "State"] = State
        df2.at[x + rows, "ZIP 5"] = Zip
        df2.at[x + rows, "Owner 1 First Name"] = One_First
        df2.at[x + rows, "Owner 1 Last Name"] = One_Last
        df2.at[x + rows, "Owner 1 Phone Numbers"] = np.nan
        df2.at[x + rows, "Owner 2 First Name"] = Two_First
        df2.at[x + rows, "Owner 2 Last Name"] = Two_Last
        df2.at[x + rows, "Owner 2 Phone Numbers"] = np.nan

df2 = df2.dropna(axis=0, how="all")
df2.to_csv("(F) " + file_location, index=False)
