import requests
import json

versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
most_recent_version = requests.get(versions_url).json()[0]
champions_url = "https://ddragon.leagueoflegends.com/cdn/" + str(most_recent_version) + "/data/en_US/champion.json"
champions = {}
champion_data = requests.get(champions_url).json()["data"]

tags = set([])
ids = set([])

for champion in list(champion_data.keys()):
    champions[int(champion_data[champion]["key"])] = champion_data[champion]