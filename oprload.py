import pandas as pd

df_opr = pd.read_csv("opr.csv")
df_opr = df_opr.rename(columns={
    "tot.value": "tot_value",
    "auto.value": "auto_value",
    "teleop.value": "teleop_value",
    "endgame.value": "endgame_value"
})
df_opr.to_csv("opr.csv", index=False)
print(df_opr.head())