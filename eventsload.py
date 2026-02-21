import json
import pandas as pd

data = []
# Load the JSON file containing all events
with open("allevents.json", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            data.append(json.loads(line))

rows = []  # will store one row per match

# Loop through each event in the dataset
for event in data:
    # Loop through matches in the event (default to empty list if missing)
    for match in event.get("matches", []):
        # Collect red alliance team numbers
        red_teams = [
            t["teamNumber"]
            for t in match.get("teams", [])
            if t["station"].startswith("R")
        ]

        # Collect blue alliance team numbers
        blue_teams = [
            t["teamNumber"]
            for t in match.get("teams", [])
            if t["station"].startswith("B")
        ]

        # Build a flat row for this match
        rows.append({
            "event": event.get("name"),                # event name
            "series": match.get("series"),             # qualification / playoff, etc.
            "matchNumber": match.get("matchNumber"),   # match number within series
            "scoreRedFinal": match.get("scoreRedFinal"),
            "scoreBlueFinal": match.get("scoreBlueFinal"),
            "redTeams": red_teams,                     # list of red team numbers
            "blueTeams": blue_teams,                   # list of blue team numbers
            # label = 1 if red wins, 0 otherwise
            "label": 1 if match.get("scoreRedFinal", 0) >
                           match.get("scoreBlueFinal", 0) else 0
        })

# Convert all rows into a pandas DataFrame
df = pd.DataFrame(rows)

# Save the flattened match data to CSV
df.to_csv("matches_flat.csv", index=False)

# Print first few rows to verify
print(df.head())
