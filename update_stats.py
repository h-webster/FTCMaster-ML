from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "myFirstDatabase"
OPR_COLLECTION = "alloprs"
MATCH_COLLECTION = "allevents"

def update_opr_csv():
    try:
        print(f"[{datetime.now()}] connecting to MongoDB")
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[OPR_COLLECTION]

        print(f"[{datetime.now()}] Fetching OPR data...")
        data = list(collection.find({}, {
            '_id': 0,  # Exclude MongoDB ID
            'number': 1,
            'tot.value': 1,
            'auto.value': 1,
            'teleop.value': 1,
            'endgame.value': 1
            # Add any other fields you need
        })) 

        flattened_data = []
        for doc in data:
            flattened_data.append({
                'number': doc.get('number'),
                'tot_value': doc.get('tot', {}).get('value', 0),
                'auto_value': doc.get('auto', {}).get('value', 0),
                'teleop_value': doc.get('teleop', {}).get('value', 0),
                'endgame_value': doc.get('endgame', {}).get('value', 0)
            })
        
         # Convert to DataFrame and save
        df = pd.DataFrame(flattened_data)
        output_path = os.path.join(os.path.dirname(__file__), 'opr.csv')
        df.to_csv(output_path, index=False)
        
        print(f"[{datetime.now()}] Successfully updated opr.csv with {len(df)} teams")
        print(f"Columns: {list(df.columns)}")
        print(f"Sample data:\n{df.head()}")
        
        client.close()
    except Exception as e:
        print(f"[{datetime.now()}] ERROR: {str(e)}")
        raise

def update_matches_csv():
    try:
        print(f"[{datetime.now()}] connecting to MongoDB")
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[MATCH_COLLECTION]

        print(f"[{datetime.now()}] Fetching OPR data...")
        events = list(collection.find({}, {
            '_id': 0,  # Exclude MongoDB ID
            'name': 1,
            'matches': 1
        })) 

        flattened_data = []

        for event in events:
            event_name = event.get('name', 'Unknown Event')
            matches = event.get('matches', [])

            for match in matches:
                series = match.get('series', 0)
                match_number = match.get('matchNumber', 0)
                score_red_final = match.get('scoreRedFinal', 0)
                score_blue_final = match.get('scoreBlueFinal', 0)
                
                # Extract team numbers for red and blue alliances
                teams = match.get('teams', [])
                red_teams = []
                blue_teams = []
                
                for team in teams:
                    team_number = team.get('teamNumber')
                    station = team.get('station', '')
                    
                    if station.startswith('Red'):
                        red_teams.append(team_number)
                    elif station.startswith('Blue'):
                        blue_teams.append(team_number)
                
                # Determine label (1 if red won, 0 if blue won)
                label = 1 if score_red_final > score_blue_final else 0
                
                flattened_data.append({
                    'event': event_name,
                    'series': series,
                    'matchNumber': match_number,
                    'scoreRedFinal': score_red_final,
                    'scoreBlueFinal': score_blue_final,
                    'redTeams': red_teams,
                    'blueTeams': blue_teams,
                    'label': label
                })
        
         # Convert to DataFrame and save
        df = pd.DataFrame(flattened_data)
        output_path = os.path.join(os.path.dirname(__file__), 'matches.csv')
        df.to_csv(output_path, index=False)
        
        print(f"[{datetime.now()}] Successfully updated matches.csv with {len(df)} teams")
        print(f"Columns: {list(df.columns)}")
        print(f"Sample data:\n{df.head()}")
        
        client.close()
    except Exception as e:
        print(f"[{datetime.now()}] ERROR: {str(e)}")
        raise



if __name__ == "__main__":
    update_opr_csv()
    update_matches_csv()