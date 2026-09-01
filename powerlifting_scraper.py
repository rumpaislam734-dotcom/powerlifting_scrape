import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.openpowerlifting.org/mlist/"

FEDERATIONS = [
    "usapl",
    "uspa",
    "ipf",
    "cpu",
    "ipa",
    "apf",
    "rps",
    "wpc",
    "spf",
    "365strong",
    "aau",
    "apa"
]

TARGET_ROWS = 2500

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_data = []

for federation in FEDERATIONS:

    url = BASE_URL + federation

    print("Scraping:", url)

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")

        if table is None:
            print("No table found:", federation)
            continue

        rows = table.find_all("tr")

        for row in rows[1:]:

            cells = row.find_all("td")

            if len(cells) < 5:
                continue

            federation_name = cells[0].get_text(strip=True)
            date = cells[1].get_text(strip=True)
            location = cells[2].get_text(" ", strip=True)
            meet_name = cells[3].get_text(" ", strip=True)
            lifters = cells[4].get_text(strip=True)

            meet_country = ""
            meet_state = ""
            meet_town = ""

            if location:

                parts = [
                    x.strip()
                    for x in location.split(",")
                    if x.strip()
                ]

                if len(parts) == 1:
                    meet_country = parts[0]

                elif len(parts) == 2:
                    meet_state = parts[0]
                    meet_country = parts[1]

                elif len(parts) >= 3:
                    meet_town = parts[0]
                    meet_state = parts[1]
                    meet_country = parts[-1]

            all_data.append({
                "Federation": federation_name,
                "Date": date,
                "MeetCountry": meet_country,
                "MeetState": meet_state,
                "MeetTown": meet_town,
                "MeetName": meet_name,
                "Lifters": lifters
            })

            if len(all_data) >= TARGET_ROWS:
                break

        if len(all_data) >= TARGET_ROWS:
            break

        time.sleep(1)

    except Exception as e:
        print("Error:", federation, e)


df = pd.DataFrame(all_data)

if df.empty:
    print("No data collected.")
    exit()

df = df.drop_duplicates()

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df["Lifters"] = pd.to_numeric(
    df["Lifters"],
    errors="coerce"
)

df["Year"] = df["Date"].dt.year

df = df.dropna(
    subset=["Date", "MeetName"]
)

df = df.reset_index(drop=True)

df.insert(
    0,
    "MeetID",
    range(1, len(df) + 1)
)

df = df.head(TARGET_ROWS)

df.to_csv(
    "powerlifting_meets_dataset.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nScraping completed!")
print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 10 rows:")
print(df.head(10))

print("\nDataset information:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum())
