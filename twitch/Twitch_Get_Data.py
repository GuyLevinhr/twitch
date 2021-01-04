import requests
import numpy as np
import time
import boto3
import testdata
import json
from datetime import datetime

# Get access_token
# url = "https://id.twitch.tv/oauth2/token?grant_type=client_credentials&client_id=swc4ajhXXXXXXXXXXXX&client_secret=dyt061XXXXXXXXXXXXXX"
# response = requests.request("POST", url)
# data = response.json()
# access_token = data['access_token']
# print(access_token)

all_games_id = []
cursor = ''
page_index = 0
games = []

stream_url = "https://api.twitch.tv/helix/streams"
game_url = "https://api.twitch.tv/helix/games"
live_url = 'https://www.twitch.tv/'

access_token = "pfbjun9XXXXXXXXXXXX"

headers = {
    'Authorization': "Bearer " + access_token,
    'Client-Id': "swc4ajh95XXXXXXXXXXXX"
}

STREAM_NAME = "twitch.stream"
REGION = "eu-north-1"

kinesis_client = boto3.client('kinesis', region_name=REGION)



while True:
    if page_index > 1001:
        page_index = 0
        time.sleep(5)
        #break

    if page_index == 0:
        live_params = {}
        cursor = ''

    else:
        live_params = {"fisrt": "20", "after": cursor}

    json_live = requests.request("GET", stream_url, headers=headers, params=live_params).json()

    cursor = json_live["pagination"]["cursor"]
    live_data = [x for x in json_live["data"] if x["game_id"]]
    new_game_ids = [x["game_id"] for x in live_data]

    Search_game = list(np.setdiff1d(new_game_ids, all_games_id))
    if Search_game:
        all_games_id.extend(Search_game)
        game_params = {"id": Search_game}

        new_games = requests.request("GET", game_url, headers=headers, params=game_params).json()
        games.extend([x for x in new_games["data"]])

    now = datetime.now()

    for l in live_data:
        game_found = next((g for g in games if g["id"] == l["game_id"]), None)
        if game_found:
            l.update({"date_and_time": str(now)})
            l.update({"game_name": game_found["name"]})
            l.update({"game_thumbnail_url": game_found["box_art_url"]})
            l.update({"live_url": live_url + l["user_name"].replace(" ", "")})
        else:
            live_data.remove(l)

    for l in live_data:
        kinesis_client.put_record(
                        StreamName=STREAM_NAME,
                        Data=json.dumps(l),
                        PartitionKey="partitionkey")

    page_index += 20
    time.sleep(1)
    #print(live_data) 
