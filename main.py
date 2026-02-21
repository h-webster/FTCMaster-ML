from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel # for validating JSON data
import pandas as pd
import joblib
from typing import List

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ftc-master-b59g.vercel.app"
        "https://www.ftcmaster.org"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# load ML model
model = joblib.load("match_predictor.pkl")

# load opr csv
df_opr = pd.read_csv("opr.csv")

# basically the schema
class MatchInput(BaseModel):
    redTeams: List[int]
    blueTeams: List[int]

def sum_opr(teams, column):
    return df_opr[df_opr["number"].isin(teams)][column].sum()

@app.post("/predict")
def predict(match: MatchInput):
    features = ["tot_diff", "auto_diff", "teleop_diff", "endgame_diff"]
    new_match = pd.DataFrame([[
        sum_opr(match.redTeams, "tot_value") - sum_opr(match.blueTeams, "tot_value"),
        sum_opr(match.redTeams, "auto_value") - sum_opr(match.blueTeams, "auto_value"),
        sum_opr(match.redTeams, "teleop_value") - sum_opr(match.blueTeams, "teleop_value"),
        sum_opr(match.redTeams, "endgame_value") - sum_opr(match.blueTeams, "endgame_value")
    ]], columns=features)

    pred_class = model.predict(new_match)[0]
    pred_prob = model.predict_proba(new_match)[0]

    return {
        "winner": "Red" if pred_class == 1 else "Blue",
        "probabilities": {"Red": pred_prob[1], "Blue": pred_prob[0]}
    }

