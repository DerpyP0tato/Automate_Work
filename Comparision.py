import pandas as pd

file_location_1 = input("Input First File: ")
# file_location_1 = "(F) 11801 5-10 - Phone Only.csv"

file_location_2 = input("Input Second File: ")
# file_location_2 = "1.csv"


df1 = pd.read_csv(r"" + file_location_1)
df2 = pd.read_csv(r"" + file_location_2)

print(df1.index)
print(df2.index)

print(df1.compare(df2))
