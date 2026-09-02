import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "powerlifting_meets_dataset.csv"
)

print("========== DATASET ==========")

print(df.head())

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())


print("\n========== FEDERATION ANALYSIS ==========")

federation_count = (
    df["Federation"]
    .value_counts()
)

print(federation_count)


print("\n========== COUNTRY ANALYSIS ==========")

country_count = (
    df["MeetCountry"]
    .value_counts()
)

print(country_count.head(15))


print("\n========== YEAR ANALYSIS ==========")

year_count = (
    df["Year"]
    .value_counts()
    .sort_index()
)

print(year_count)


print("\n========== TOP MEETS BY LIFTERS ==========")

top_meets = (
    df.sort_values(
        "Lifters",
        ascending=False
    )
    [["MeetName", "Federation", "MeetCountry", "Lifters"]]
    .head(10)
)

print(top_meets)


# ----------------------------------
# GRAPH 1
# Federation
# ----------------------------------

plt.figure(figsize=(10, 6))

federation_count.head(10).plot(
    kind="bar"
)

plt.title(
    "Top 10 Powerlifting Federations"
)

plt.xlabel("Federation")

plt.ylabel("Number of Meets")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "federation_analysis.png"
)

plt.show()


# ----------------------------------
# GRAPH 2
# Country
# ----------------------------------

plt.figure(figsize=(10, 6))

country_count.head(10).plot(
    kind="bar"
)

plt.title(
    "Top 10 Countries by Number of Meets"
)

plt.xlabel("Country")

plt.ylabel("Number of Meets")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "country_analysis.png"
)

plt.show()


# ----------------------------------
# GRAPH 3
# Year
# ----------------------------------

plt.figure(figsize=(10, 6))

year_count.plot(
    kind="line",
    marker="o"
)

plt.title(
    "Powerlifting Meets by Year"
)

plt.xlabel("Year")

plt.ylabel("Number of Meets")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "year_analysis.png"
)

plt.show()


# ----------------------------------
# GRAPH 4
# Lifters
# ----------------------------------

top_lifters = (
    df.sort_values(
        "Lifters",
        ascending=False
    )
    .head(10)
)

plt.figure(figsize=(12, 6))

plt.bar(
    top_lifters["MeetName"],
    top_lifters["Lifters"]
)

plt.title(
    "Top 10 Meets by Number of Lifters"
)

plt.xlabel("Meet")

plt.ylabel("Number of Lifters")

plt.xticks(
    rotation=75,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    "top_meets_analysis.png"
)

plt.show()
