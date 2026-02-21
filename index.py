from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mangum import Mangum
from pymongo import MongoClient
import joblib
from typing import List
import os
from dotenv import load_dotenv
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
load_dotenv()
# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["myFirstDatabase"]
opr_collection = db["alloprs"]

# Load ML model
base_path = os.path.dirname(__file__)
model = joblib.load(os.path.join(base_path, "match_predictor.pkl"))

class MatchInput(BaseModel):
    redTeams: List[int]
    blueTeams: List[int]

def get_team_opr(team_number: int):
    """Fetch a single team's OPR data from MongoDB"""
    return opr_collection.find_one({"number": team_number})

def sum_opr(teams: List[int], nested_field: str):
    """
    Sum OPR values for a list of teams.
    nested_field uses dot notation e.g. 'tot.value', 'auto.value'
    """
    total = 0
    parts = nested_field.split(".")
    for team in teams:
        doc = get_team_opr(team)
        if doc:
            val = doc
            for p in parts:
                val = val.get(p, 0)
            total += val
    return total

@app.get("/")
def root():
    return {"status": "FTC Match Predictor API is running"}

@app.get("/teams/{team_number}")
def get_team(team_number: int):
    """Get a team's OPR data"""
    team = opr_collection.find_one({"number": team_number}, {"_id": 0})
    return team or {"error": "Team not found"}

@app.post("/predict")
def predict(match: MatchInput):
    features = ["tot_diff", "auto_diff", "teleop_diff", "endgame_diff"]

    red_tot = sum_opr(match.redTeams, "tot.value")
    blue_tot = sum_opr(match.blueTeams, "tot.value")
    red_auto = sum_opr(match.redTeams, "auto.value")
    blue_auto = sum_opr(match.blueTeams, "auto.value")
    red_teleop = sum_opr(match.redTeams, "teleop.value")
    blue_teleop = sum_opr(match.blueTeams, "teleop.value")
    red_endgame = sum_opr(match.redTeams, "endgame.value")
    blue_endgame = sum_opr(match.blueTeams, "endgame.value")

    new_match = [[
        red_tot - blue_tot,
        red_auto - blue_auto,
        red_teleop - blue_teleop,
        red_endgame - blue_endgame
    ]]

    pred_class = model.predict(new_match)[0]
    pred_prob = model.predict_proba(new_match)[0]

    return {
        "winner": "Red" if pred_class == 1 else "Blue",
        "probabilities": {
            "Red": float(pred_prob[1]),
            "Blue": float(pred_prob[0])
        },
        "oprs": {
            "red": {"total": red_tot, "auto": red_auto, "teleop": red_teleop, "endgame": red_endgame},
            "blue": {"total": blue_tot, "auto": blue_auto, "teleop": blue_teleop, "endgame": blue_endgame}
        }
    }

# Vercel handler
app_handler = Mangum(app)