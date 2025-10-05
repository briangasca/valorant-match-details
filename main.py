from valclient.client import Client
import time
from rich.table import Table
from rich.console import Console
from constants import agentMap, rankMap

## for later: use https://valorant-api.com/v1/weapons for skins matching Uuids
##note: must be in an active game to use!

class Player:
    def __init__(self, client, puuid, agentID, team, incognito, level):
        self.client = client
        self.puuid = puuid
        self.agentID = agentID
        self.team = team
        self.incognito = incognito
        self.level = level
        self.agent = self.getAgent(self.agentID)
        self.gameName = self.getNameEndpoint(self.puuid)
        self.rank = self.getRank(puuid)

    def getRank(self, puuid):
        mmr = client.fetch_mmr(puuid)
        seasonal_info = mmr["QueueSkills"]["competitive"]["SeasonalInfoBySeasonID"]

        if seasonal_info and isinstance(seasonal_info, dict) and len(seasonal_info) > 0:
            latest_season = list(seasonal_info.values())[-1]
            tier = latest_season.get("CompetitiveTier", 0)
            return rankMap.get(tier, "Unrated")
        

    def getNameEndpoint(self, puuid):
        playerData = self.client.put(
            endpoint="/name-service/v2/players", 
            endpoint_type="pd", 
            json_data=[puuid]
        )[0]
        return f"{playerData['GameName']}#{playerData['TagLine']}"

    def getAgent(self, agentID):
        return agentMap[agentID]

client = Client(region="na")
client.activate()

curr_game = client.coregame_fetch_match()['MatchID']
matchInfo = client.coregame_fetch_match(curr_game)
loadouts = client.coregame_fetch_match_loadouts()
players = matchInfo['Players']

active_player_objects = []

for player in players:
    active_player_objects.append(Player(
        client,
        player['Subject'].lower(),
        player['CharacterID'].lower(),
        player['TeamID'].lower(),
        player['PlayerIdentity']['Incognito'],
        player['PlayerIdentity']['AccountLevel']
        
    ))

##cmd table

console = Console()
table = Table(title="Valorant Match Details")

table.add_column("Game Name", justify="left")
table.add_column("Agent", justify="center")
table.add_column("Name Hidden?")
table.add_column("Rank")
table.add_column("Level", justify="right")

for player in active_player_objects:
    if player.team == "blue":
        table.add_row(f"[bright_blue]{player.gameName}[/bright_blue]", f"[bright_blue]{player.agent}[/bright_blue]", str(player.incognito), player.rank, str(player.level))
    else:
        table.add_row(f"[bright_red]{player.gameName}[/bright_red]", f"[bright_red]{player.agent}[/bright_red]", str(player.incognito), player.rank, str(player.level))
console.print(table)
