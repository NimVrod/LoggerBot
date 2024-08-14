import json
import os

first_time = {"VoiceLogs": 0}

def create_database(guild_id: int) -> None:
    with open(f"Storage/{guild_id}.json", "w") as file:
        json.dump(first_time, file, indent=4)

def write_database(guild_id: int, db: dict) -> None:
    with open(f"Storage/{guild_id}.json", "w") as file:
        json.dump(db, file, indent=4)

def read_database(guild_id: int) -> dict:
    with open(f"Storage/{guild_id}.json", "r") as file:
        return json.load(file)

def check_if_guild_in_db(guild_id: int) -> bool:
    return os.path.exists(f"Storage/{guild_id}.json")

def check_for_changes():
    for filename in os.listdir("Storage"):
        if filename.endswith(".json"):
            filepath = f"Storage/{filename}"
            with open(filepath, "r") as file:
                db = json.load(file)
                for key in first_time:
                    if key not in db:
                        db[key] = first_time[key]
                        write_database(int(filename.split('.')[0]), db)