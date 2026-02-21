import pandas as pd
import joblib

# Load OPR CSV
df_opr = pd.read_csv("opr.csv").set_index("number")

# Load trained model
model = joblib.load("match_predictor.pkl")

# Sum a column for a list of team numbers
def sum_opr(teams, column):
    return df_opr.loc[teams, column].sum()

# Check if team exists and has non-zero OPR
def has_valid_opr(team):
    return team in df_opr.index and df_opr.at[team, "tot_value"] != 0.0

# --- Interactive input ---
while True:
    red_input = input("Enter Red team numbers separated by commas (e.g. 3491,10517): ")
    if red_input.lower() == "exit":
        break

    try:
        red_teams = [int(t.strip()) for t in red_input.split(",")]
    except ValueError:
        print("Invalid input format.")
        continue

    if len(red_teams) != 2:
        print("Please enter exactly 2 Red teams.")
        continue

    if any(not has_valid_opr(t) for t in red_teams):
        print("One or more Red teams not found or have zero OPR.")
        continue

    blue_input = input("Enter Blue team numbers separated by commas (e.g. 11143,11144): ")
    if blue_input.lower() == "exit":
        break

    try:
        blue_teams = [int(t.strip()) for t in blue_input.split(",")]
    except ValueError:
        print("Invalid input format.")
        continue

    if len(blue_teams) != 2:
        print("Please enter exactly 2 Blue teams.")
        continue

    if any(not has_valid_opr(t) for t in blue_teams):
        print("One or more Blue teams not found or have zero OPR.")
        continue

    # Compute feature vector
    features = ["tot_diff", "auto_diff", "teleop_diff", "endgame_diff"]

    new_match = pd.DataFrame([[
        sum_opr(red_teams, "tot_value")     - sum_opr(blue_teams, "tot_value"),
        sum_opr(red_teams, "auto_value")    - sum_opr(blue_teams, "auto_value"),
        sum_opr(red_teams, "teleop_value")  - sum_opr(blue_teams, "teleop_value"),
        sum_opr(red_teams, "endgame_value") - sum_opr(blue_teams, "endgame_value")
    ]], columns=features)

    # Predict
    pred_class = model.predict(new_match)[0]
    pred_prob = model.predict_proba(new_match)[0]

    print(f"\nPredicted winner: {'Red' if pred_class == 1 else 'Blue'}")
    print(f"Probability: Red win={pred_prob[1]:.2f}, Blue win={pred_prob[0]:.2f}\n")
