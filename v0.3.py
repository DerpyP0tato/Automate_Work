import pandas as pd
import numpy as np

debug = True

file_location = input("Input File Location: ")

DNC_Count = 0
DC_Count = 0

row_nums = 0

df = pd.read_csv(r"" + file_location)

df2 = pd.DataFrame().reindex_like(df).dropna(axis=0, how="all")

DNC_List = []

DC_List = []


def removeDNC(PN_List):
    global DNC_Count, DC_Count
    DC_Number = []
    if type(PN_List) == str:
        PN_List = PN_List.split(", ")
        for y in range(len(PN_List)):
            if "DNC" not in PN_List[y]:
                DC_Count += 1
                DC_Number.append(PN_List[y])
                DC_List.append(PN_List[y])
            else:
                DNC_Count += 1
                DNC_List.append(PN_List[y])
    return DC_Number


for x in df.index:
    One_Phone = df.at[x, "Owner 1 Phone Numbers"]
    Two_Phone = df.at[x, "Owner 2 Phone Numbers"]

    df.at[x, "Owner 1 Phone Numbers"] = removeDNC(One_Phone)

    df.at[x, "Owner 2 Phone Numbers"] = removeDNC(Two_Phone)


def ownerOne(row_num, OF=np.nan, OL=np.nan, OP=np.nan):
    df2.at[row_num, "Owner 1 First Name"] = OF
    df2.at[row_num, "Owner 1 Last Name"] = OL
    df2.at[row_num, "Owner 1 Phone Numbers"] = OP


def ownerTwo(row_num, OF=np.nan, OL=np.nan, OP=np.nan):
    df2.at[row_num, "Owner 2 First Name"] = OF
    df2.at[row_num, "Owner 2 Last Name"] = OL
    df2.at[row_num, "Owner 2 Phone Numbers"] = OP


def default(row_num, A, C, S, Z):
    df2.at[row_num, "Property Address"] = A
    df2.at[row_num, "City"] = C
    df2.at[row_num, "State"] = S
    df2.at[row_num, "ZIP 5"] = Z


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
            row = len(df2.index) + 1
            default(row_num=row, A=Address, C=City, S=State, Z=Zip)
            if i < len(One_Phone):
                ownerOne(row_num=row, OF=One_First, OL=One_Last, OP=One_Phone[i])
            elif i == 0:
                ownerOne(row_num=row, OF=One_First, OL=One_Last)
            else:
                ownerOne(row_num=row)
            if i < len(Two_Phone):
                ownerTwo(row_num=row, OF=Two_First, OL=Two_Last, OP=Two_Phone[i])
            elif i == 0:
                ownerTwo(row_num=row, OF=Two_First, OL=Two_Last)
            else:
                ownerTwo(row_num=row)
            row_nums += 1
    else:
        row = len(df2.index) + 1
        default(row_num=row, A=Address, C=City, S=State, Z=Zip)
        ownerOne(row_num=row, OF=One_First, OL=One_Last)
        ownerTwo(row_num=row, OF=Two_First, OL=Two_Last)

print(f"{DC_Count} phone numbers saved")
print(f"{DNC_Count} phone numbers deleted.")

df2.to_csv(r"(F) " + str(file_location), index=False)
print(f"""File "(F) {file_location}" has been created.""")

if debug is True:
    DNC_df = pd.DataFrame(DNC_List, columns=['DNC Numbers'])
    DNC_df.to_csv(r"(DNC) " + str(file_location), index=False)
    print(f"""File "(DNC) {file_location}" has been created.""")
    DC_df = pd.DataFrame(DC_List, columns=['DNC Numbers'])
    DC_df.to_csv(r"(DC) " + str(file_location), index=False)
    print(f"""File "(DC) {file_location}" has been created.""")
