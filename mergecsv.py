import pandas as pd

df_matches = pd.read_csv("matches.csv")
df_opr = pd.read_csv("opr.csv")

def sum_opr(teams, column):
    return df_opr[df_opr["number"].isin(teams)][column].sum()

# Create new columns for red and blue alliance OPR sums
df_matches["red_tot_opr"] = df_matches["redTeams"].apply(lambda x: sum_opr(eval(x), "tot_value"))
df_matches["blue_tot_opr"] = df_matches["blueTeams"].apply(lambda x: sum_opr(eval(x), "tot_value"))
print("1")

df_matches["red_auto_opr"] = df_matches["redTeams"].apply(lambda x: sum_opr(eval(x), "auto_value"))
df_matches["blue_auto_opr"] = df_matches["blueTeams"].apply(lambda x: sum_opr(eval(x), "auto_value"))
print("2")

df_matches["red_teleop_opr"] = df_matches["redTeams"].apply(lambda x: sum_opr(eval(x), "teleop_value"))
df_matches["blue_teleop_opr"] = df_matches["blueTeams"].apply(lambda x: sum_opr(eval(x), "teleop_value"))
print("3")

df_matches["red_endgame_opr"] = df_matches["redTeams"].apply(lambda x: sum_opr(eval(x), "endgame_value"))
df_matches["blue_endgame_opr"] = df_matches["blueTeams"].apply(lambda x: sum_opr(eval(x), "endgame_value"))
print("4")

# Create difference features (optional, helps ML learn better)
df_matches["tot_diff"] = df_matches["red_tot_opr"] - df_matches["blue_tot_opr"]
df_matches["auto_diff"] = df_matches["red_auto_opr"] - df_matches["blue_auto_opr"]
df_matches["teleop_diff"] = df_matches["red_teleop_opr"] - df_matches["blue_teleop_opr"]
df_matches["endgame_diff"] = df_matches["red_endgame_opr"] - df_matches["blue_endgame_opr"]
print("5")

# Select only features + label for ML
ml_df = df_matches[["tot_diff", "auto_diff", "teleop_diff", "endgame_diff", "label"]]
# label: 1 = Red wins, 0 = Blue wins

# Save ML-ready CSV
ml_df.to_csv("ml_matches.csv", index=False)

print(ml_df.head())