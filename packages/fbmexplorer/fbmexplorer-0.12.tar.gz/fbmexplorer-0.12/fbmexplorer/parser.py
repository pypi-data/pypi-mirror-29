import json
import pandas as pd
from pandas.io.json import json_normalize
import sys

def parse(file):

    with open(file) as f:
        d = json.load(f)

    user_name = d['user']
    df = json_normalize(d, ["threads", "messages"], [["threads", "participants"]], errors="ignore")
    df["sent"] = df["sender"] == user_name
    df["length"] = df["message"].str.len()
    df.to_json("flat_messages.json", orient="table") # Full file

    # Add the user name to the full file
    with open("flat_messages.json", "r") as f:
        d = json.load(f)
    d['user'] = user_name
    with open("flat_messages.json", "w") as f:
        json.dump(d, f)

if __name__ == '__main__':
    parse(sys.argv[1])
