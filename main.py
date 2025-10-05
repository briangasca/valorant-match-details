from valclient.client import Client
from colorama import init, Fore, Style
from tqdm import tqdm
import time
from constants import agentMap, rankMap

## for later: use https://valorant-api.com/v1/weapons for skins matching Uuids

##note: must be in an active game to use!

client = Client(region="na")
client.activate()

curr_game = client.coregame_fetch_match()['MatchID']
matchInfo = client.coregame_fetch_match(curr_game)
loadouts = client.coregame_fetch_match_loadouts()
players = matchInfo['Players']

class Player:
    def __init__(self, client, puuid, agentID):
        self.client = client
        self.puuid = puuid
        self.agentID = agentID
        self.agent = self.getAgent(self.agentID)
        self.gameName = self.getNameEndpoint(self.puuid)

    def getNameEndpoint(self, puuid):
        playerData = self.client.put(
            endpoint="/name-service/v2/players", 
            endpoint_type="pd", 
            json_data=[puuid]
        )[0]
        return f"{playerData['GameName']}#{playerData['TagLine']}"

    def getAgent(self, agentID):
        return agentMap[agentID]


active_player_objects = []

for player in players:
    active_player_objects.append(Player(
        client,
        player['Subject'].lower(),
        player['CharacterID'].lower()
    ))

print("- Game Name -- Agent --")
for player in active_player_objects:
    print(f"| {player.gameName} | {player.agent}")
print("----------------------------")
