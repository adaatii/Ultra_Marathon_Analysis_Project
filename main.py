import pandas as pd
import seaborn as sns

df = pd.read_csv("TWO_CENTURIES_OF_UM_RACES.csv")

# See the data that's been imported
# print(df.head(10))
print("SHAPE")
print(df.shape)
print("DTYPES")
print(df.dtypes)

# Clean up data
# Only the USA Races, 50k and 50Mi, 2020
# Step 1 - Show 50K or 50Mi
# print(df[(df['Event distance/length'].isin(['50mi','50km'])) & (df['Year of event'] == 2020)])
# print(df[df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA'])

# Combine all the filters
df2 = df[
    (df["Event distance/length"].isin(["50mi", "50km"]))
    & (df["Year of event"] == 2020)
    & (df["Event name"].str.split("(").str.get(1).str.split(")").str.get(0) == "USA")
]

# Remove (USA) from the Event name
df2["Event name"] = df2["Event name"].str.split("(").str.get(0)

# Clean up athlete age
df2['athlete_age'] = 2020 - df2['Athlete year of birth']

# Remove h from athlete performance
df2['Athlete performance'] = df2['Athlete performance'].str.split(' ').str.get(0)

# Drop columns: Athlete Club, Athlete Country, Athlete year of birth, Athlete Age Category 

df2.drop(columns=['Athlete club', 'Athlete country', 'Athlete year of birth', 'Athlete age category'], axis=1)
print(df2.head(10))
