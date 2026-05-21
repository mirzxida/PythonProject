import os
import json

save_path = "data/save.json"

def load():
    if not os.path.exists(save_path):
        return {"high_score": 0}
    with open(save_path, "r") as f:
        return json.load(f)

def save(data):
    os.makedirs("data", exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(data, f, indent=4)