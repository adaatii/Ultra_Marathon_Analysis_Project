import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("TWO_CENTURIES_OF_UM_RACES.csv")

# See the data that's been imported
print(df.head(10))
print("SHAPE")
print(df.shape)
print("DTYPES")
print(df.dtypes)

# Clean up data
# Only the USA Races, 50k and 50Mi, 2020
# Step 1 - Show 50K or 50Mi

#print(df[(df['Event distance/length'].isin(['50mi','50km'])) & (df['Year of event'] == 2020)])
#print(df[df['Event name'].str.split('(').str.get(1).str.split(')').str.get(0) == 'USA'])

# Combine all the filters
df2 = df[
    (df["Event distance/length"].isin(["50mi", "50km"]))
    & (df["Year of event"] == 2020)
    & (df["Event name"].str.replace("(USA)", ""))
].copy()

# Remove (USA) from the Event name
df2["Event name"] = df2["Event name"].str.split("(").str.get(0)

# Clean up athlete age
df2["athlete_age"] = 2020 - df2["Athlete year of birth"]

# Remove h from athlete performance
df2["Athlete performance"] = df2["Athlete performance"].str.split(" ").str.get(0)

# Drop columns: Athlete Club, Athlete Country, Athlete year of birth, Athlete Age Category

df2.drop(
    columns=[
        "Athlete club",
        "Athlete country",
        "Athlete year of birth",
        "Athlete age category",
    ],
    axis=1,
)

# Clean up null values
df2.isnull().sum()

# Drop rows with null values
df2.dropna(inplace=True)

# Drop duplicates
df2.drop_duplicates()

# Reset index
df2.reset_index(drop=True)

# Fix data types
df2["athlete_age"] = df2["athlete_age"].astype(int)
df2["Athlete average speed"] = df2["Athlete average speed"].astype(float)

# Rename columns
df2 = df2.rename(
    columns={
        "Year of event": "year",
        "Event dates": "race_date",
        "Event name": "race_name",
        "Event distance/length": "race_distance",
        "Event number of finishers": "num_finishers",
        "Athlete performance": "athlete_performance",
        "Athlete club": "athlete_club",
        "Athlete country": "athlete_country",
        "Athlete year of birth": "athlete_year_of_birth",
        "Athlete gender": "athlete_gender",
        "Athlete age category": "category",
        "Athlete average speed": "athlete_avg_speed",
        "Athlete ID": "athlete_id",
    }
)

# Reorder columns
df3 = df2[
    [
        "race_date",
        "race_name",
        "race_distance",
        "num_finishers",
        "athlete_id",
        "athlete_gender",
        "athlete_age",
        "athlete_performance",
        "athlete_avg_speed",
        "category",
        "athlete_club",
        "athlete_country",
        "athlete_year_of_birth",
        "year",
    ]
].copy()

print(df3[df3["race_name"] == "Everglades 50 Mile Ultra Run "])
print(df3[df3["athlete_id"] == 222509])

# Difference in speed for 50mi and 50km male to female
print(df3.groupby(['race_distance', 'athlete_gender'])['athlete_avg_speed'].mean())

# What age groups are the best in the 50mi Race (20 + race min)
print(df3.query('race_distance == "50mi"').groupby('athlete_age')['athlete_avg_speed'].agg(['mean','count']).sort_values('mean', ascending = False).query('count>19').head(20))

# What age groups are the worst in the 50mi Race (15 + race min)
print(df3.query('race_distance == "50mi"').groupby('athlete_age')['athlete_avg_speed'].agg(['mean','count']).sort_values('mean', ascending = True).query('count>9').head(15))

# Seasons for the data -> Slower in summer than winter ?

# Spring 3-5
# Summer 6-8
# Fall 9-11
# Winter 12-2

# Split between two decimals

df3["race_month"] = df3["race_date"].str.split(".").str.get(1).astype(int).abs()

df3["race_season"] = df3["race_month"].apply(
    lambda x: "Winter"
    if x > 11
    else "Fall"
    if x > 8
    else "Summer"
    if x > 5
    else "Spring"
    if x > 2
    else "Winter"
)

print(df3.groupby('race_season')['athlete_avg_speed'].agg(['mean', 'count']).sort_values('mean', ascending=False))

# Chart the distance
fig, axes = plt.subplots(2, figsize=(15, 10))

sns.histplot(df3, x ='race_distance', hue = 'athlete_gender', ax=axes[0])
axes[0].set_title("Race Distance")

sns.violinplot(data = df3, x = 'race_distance', y = 'athlete_age',hue = 'athlete_gender', split = True, inner = 'quartile', linewidth = 1, ax=axes[1])
axes[1].set_title("Athlete Age")

plt.tight_layout()

sns.displot(df3[df3['race_distance'] == '50mi']['athlete_avg_speed'])
plt.title("50mi Average Speed")

sns.lmplot(data = df3, x = 'athlete_age', y = 'athlete_avg_speed', hue = 'athlete_gender')
plt.title("Age vs Speed")

plt.show()
