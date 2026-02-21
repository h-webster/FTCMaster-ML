import json
import pandas as pd

data = []

with open("alloprs.json", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            data.append(json.loads(line))

rows = []

for team in data:
    rows.append({
        "number": team.get("number"),
        "tot_value": team.get("tot").get("value"),
        "tot_rank": team.get("tot").get("rank"),
        "auto_value": team.get("auto").get("value"),
        "auto_rank": team.get("auto").get("rank"),
        "teleop_value": team.get("teleop").get("value"),
        "teleop_rank": team.get("teleop").get("rank"),
        "endgame_value": team.get("endgame").get("value"),
        "endgame_rank": team.get("endgame").get("rank"),
    })

df = pd.DataFrame(rows)

df.to_csv("opr_flat.csv", index=False)

print(df.head())