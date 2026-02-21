from pymongo import MongoClient
import requests
import os
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI")
FTC_API_KEY = os.getenv("FTC_API_KEY")

def fetch_match_data():
    # Fetch from FTC API or your data source
    # https://ftc-events.firstinspires.org/services/API
    pass

def calculate_opr(matches):
    # Your OPR calculation logic
    pass

def update_mongodb():
    client = MongoClient(MONGO_URI)
    db = client["ftc_data"]
    
    # Fetch and calculate
    matches = fetch_match_data()
    opr_data = calculate_opr(matches)
    
    # Update MongoDB
    for team in opr_data:
        db.team_opr.update_one(
            {"number": team["number"]},
            {"$set": team},
            upsert=True
        )
    
    print(f"Updated {len(opr_data)} teams at {datetime.now()}")

if __name__ == "__main__":
    update_mongodb()