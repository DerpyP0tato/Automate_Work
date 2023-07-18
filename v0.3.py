import pandas as pd
import numpy as np

# Settings
debug = True

# Get file location
file_location = input("Input File Location: ")

# Counting the Do Call and Do Not Call Numbers
DNC_Count = 0
DC_Count = 0

# Reads CSV file
df = pd.read_csv(rf"{file_location}")

# Creates output dataframe
df2 = pd.DataFrame().reindex_like(df).dropna(axis=0, how="all")

# Lists to store Do Not Call (DNC) and Do Call (DC) Numbers
DNC_List = []
DC_List = []


# Remove Do Not Call (DNC) Numbers from the sheet
def removeDNC(PN_List):
    global DNC_Count, DC_Count
    # Create an empty list to hold the valid Do Call (DC) numbers
    DC_Number = []
    # Find cells containing phone number(s)
    if type(PN_List) == str:
        # Separate each phone number in a cell
        PN_List = PN_List.split(", ")
        # Loop through each phone number
        for y in range(len(PN_List)):
            # Find if "DNC" marker is in the phone number
            # If there isn't a "DNC" marker...
            if "DNC" not in PN_List[y]:
                # Increment the DC counter
                DC_Count += 1
                # Add the number to the new cell
                DC_Number.append(PN_List[y])
                # Saves the number to the DC_List
                DC_List.append(PN_List[y])
            # If there is a "DNC" marker...
            else:
                # Increment the DNC counter
                DNC_Count += 1
                # Save the number to the DNC_List
                DNC_List.append(PN_List[y])
    # Output the new, filtered cell containing Do Call (DC) numbers
    return DC_Number


# Loop through each row in the original sheet
for x in df.index:
    # Locates the position of the two cells containing the phone number(s)
    One_Phone = df.at[x, "Owner 1 Phone Numbers"]
    Two_Phone = df.at[x, "Owner 2 Phone Numbers"]

    # Remove any Do Not Call (DNC) marked numbers from the respective cells
    df.at[x, "Owner 1 Phone Numbers"] = removeDNC(One_Phone)
    df.at[x, "Owner 2 Phone Numbers"] = removeDNC(Two_Phone)


# Sets appropriate values to Owner 1's information
def ownerOne(row_num, OF=np.nan, OL=np.nan, OP=np.nan):
    df2.at[row_num, "Owner 1 First Name"] = OF
    df2.at[row_num, "Owner 1 Last Name"] = OL
    df2.at[row_num, "Owner 1 Phone Numbers"] = OP


# Sets appropriate values to Owner 2's information
def ownerTwo(row_num, OF=np.nan, OL=np.nan, OP=np.nan):
    df2.at[row_num, "Owner 2 First Name"] = OF
    df2.at[row_num, "Owner 2 Last Name"] = OL
    df2.at[row_num, "Owner 2 Phone Numbers"] = OP


# Sets appropriate values for the property information
def default(row_num, A, C, S, Z):
    df2.at[row_num, "Property Address"] = A
    df2.at[row_num, "City"] = C
    df2.at[row_num, "State"] = S
    df2.at[row_num, "ZIP 5"] = Z


# Adds the row and values for formatting
# Loops through each row
for x in df.index:
    # Find the information needed in the original sheet and store them into separate variables
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

    # Checks if there are any phone numbers in the designated cells
    # If a number is found in any of the cells...
    if len(One_Phone) or len(Two_Phone) > 0:
        # Loop through the cells
        # The number of times the cells will be looped depends on the length of the cell that has the most numbers within
        for i in range(0, max(len(One_Phone), len(Two_Phone))):
            # Assign a row value where new cells will be located
            row = len(df2.index) + 1
            # Add the appropriate property information to the row
            default(row_num=row, A=Address, C=City, S=State, Z=Zip)

            # Check if there are any phone numbers left for Owner 1
            # If there are still number(s) to be inputted for Owner 1...
            if i < len(One_Phone):
                # Add the name of Owner 1 but leave the phone number cell empty
                ownerOne(row_num=row, OF=One_First, OL=One_Last, OP=One_Phone[i])
            # If there isn't a phone number, but it's the first row of the address...
            elif i == 0:

                ownerOne(row_num=row, OF=One_First, OL=One_Last)
            # If there aren't any phone numbers to be inputted
            else:
                # Leave the name and the phone number cell empty
                ownerOne(row_num=row)

            # Check if there are any phone numbers left for Owner 2
            # If there are still number(s) to be inputted for Owner 2...
            if i < len(Two_Phone):
                # Add the name of Owner 1 and the appropriate phone number
                ownerTwo(row_num=row, OF=Two_First, OL=Two_Last, OP=Two_Phone[i])
            # If there isn't a phone number, but it's the first row of the address...
            elif i == 0:
                # Add the name of Owner 2 but leave the phone number cell empty
                ownerTwo(row_num=row, OF=Two_First, OL=Two_Last)
            # If there aren't any phone number to be inputted
            else:
                # Leave the name and the phone number cell empty
                ownerTwo(row_num=row)
    # If there aren't any numbers in either cells...
    else:
        # Assigns a row value where new cells will be located
        row = len(df2.index) + 1
        # Add the appropriate property information to the row
        default(row_num=row, A=Address, C=City, S=State, Z=Zip)
        # Add names of Owner 1 and 2, leaving the phone number cells empty
        ownerOne(row_num=row, OF=One_First, OL=One_Last)
        ownerTwo(row_num=row, OF=Two_First, OL=Two_Last)

# Displays how many phone numbers were saved and deleted
print(f"{DC_Count} phone numbers saved")
print(f"{DNC_Count} phone numbers deleted.")

# Creates the filtered CSV file
df2.to_csv(r"(F) " + str(file_location), index=False)
print(f"""File "(F) {file_location}" has been created.""")

# Setting
if debug is True:
    # Creates sheets that contain all the DNC and DC phone numbers
    DNC_df = pd.DataFrame(DNC_List, columns=['DNC Numbers'])
    DNC_df.to_csv(r"(DNC) " + str(file_location), index=False)
    print(f"""File "(DNC) {file_location}" has been created.""")
    DC_df = pd.DataFrame(DC_List, columns=['DNC Numbers'])
    DC_df.to_csv(r"(DC) " + str(file_location), index=False)
    print(f"""File "(DC) {file_location}" has been created.""")

# Remove if-else statement
