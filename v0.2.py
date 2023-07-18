import pandas as pd
import numpy as np

file_location = input("Input File Location: ")

DNC_Count = 0
DC_Count = 0

rows = 0

df = pd.read_csv(r"" + file_location)

df2 = pd.DataFrame().reindex_like(df)


def removeDNC(Old):
    global DNC_Count, DC_Count
    New = []
    if type(Old) == str:
        Old = Old.split(", ")
        for y in range(len(Old)):
            if "DNC" not in Old[y]:
                DC_Count += 1
                New.append(Old[y])
            else:
                DNC_Count += 1
    return New


for x in df.index:
    One_Phone = df.at[x, "Owner 1 Phone Numbers"]
    Two_Phone = df.at[x, "Owner 2 Phone Numbers"]

    df.at[x, "Owner 1 Phone Numbers"] = removeDNC(One_Phone)

    df.at[x, "Owner 2 Phone Numbers"] = removeDNC(Two_Phone)


def ownerOne(count, OF=np.nan, OL=np.nan, OP=np.nan):
    df2.at[count + rows, "Owner 1 First Name"] = OF
    df2.at[count + rows, "Owner 1 Last Name"] = OL
    df2.at[count + rows, "Owner 1 Phone Numbers"] = OP


def ownerTwo(count, OF=np.nan, OL=np.nan, OP=np.nan):
    df2.at[count + rows, "Owner 2 First Name"] = OF
    df2.at[count + rows, "Owner 2 Last Name"] = OL
    df2.at[count + rows, "Owner 2 Phone Numbers"] = OP


def default(count, A, C, S, Z):
    df2.at[count + rows, "Property Address"] = A
    df2.at[count + rows, "City"] = C
    df2.at[count + rows, "State"] = S
    df2.at[count + rows, "ZIP 5"] = Z


for x in df.index:
    Address = df.at[x, "Property Address"]
    City = df.at[x, "City"]
    State = df.at[x, "State"]
    Zip = df.at[x, "ZIP 5"]
    One_First = df.at[x, "Owner 1 First Name"]
    One_Last = df.at[x, "Owner 1 Last Name"]
    One_Phone = df.at[x, "Owner 1 Phone Numbers"]
    Two_First = df.at[x, "Owner 2 First Name"]
    Two_Last = df.at[x, "Owner 2 Last Name"]
    Two_Phone = df.at[x, "Owner 2 Phone Numbers"]

    if len(One_Phone) or len(Two_Phone) > 0:
        for i in range(0, max(len(One_Phone), len(Two_Phone))):
            default(count=x, A=Address, C=City, S=State, Z=Zip)
            if i < len(One_Phone):
                ownerOne(count=x, OF=One_First, OL=One_Last, OP=One_Phone[i])
            elif i == 0:
                ownerOne(count=x, OF=One_First, OL=One_Last)
            else:
                ownerOne(count=x)
            if i < len(Two_Phone):
                ownerTwo(count=x, OF=Two_First, OL=Two_Last, OP=Two_Phone[i])
            elif i == 0:
                ownerTwo(count=x, OF=Two_First, OL=Two_Last)
            else:
                ownerTwo(count=x)
            rows += 1
    else:
        default(count=x, A=Address, C=City, S=State, Z=Zip)
        ownerOne(count=x, OF=One_First, OL=One_Last)
        ownerTwo(count=x, OF=Two_First, OL=Two_Last)

df2 = df2.dropna(axis=0, how="all")

print(f"{DC_Count} phone numbers saved")
print(f"{DNC_Count} phone numbers deleted.")

df2.to_csv("(NF) " + file_location, index=False)
print(f"""File "(NF) {file_location}" has been created.""")

# put dnc in separate sheet
