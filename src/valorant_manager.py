from valclient.client import Client 
import os
from operator import itemgetter

from .content_loader import Loader

class Valorant:

    cur_path = os.path.dirname(__file__)
    file_path = os.path.join(cur_path,"../match_reference.json")

    def __init__(self):
        self.client = Client() 
        self.client.activate()

    def load_match_data(self):
        # agent images are from https://playvalorant.com/page-data/en-us/agents/page-data.json
        content = Loader.load_all_content(self.client)
        matches = self.client.fetch_match_history()["History"]
        match_data = self.client.fetch_match_details(matches[0]["MatchID"])
        
        total_rounds = len(match_data["roundResults"])

        payload = {
            "match_id": match_data["matchInfo"]["matchId"],
            "match_map": match_data["matchInfo"]["mapId"],
            "match_mode": match_data["matchInfo"]["queueID"],
            "match_mode_display_name": content["queue_aliases"][match_data["matchInfo"]["queueID"]],
            "match_map_display_name": [gmap for gmap in content["maps"] if match_data["matchInfo"]["mapId"] in gmap["path"]][0]["display_name"],
            "teams": [
                {
                    "team_name": team["teamId"],
                    "team_alias": "ATK" if team["teamId"] == "Red" else "DEF",
                    "won_bool": team["won"],
                    "won": "WIN" if team["won"] else "LOSS",
                    "rounds_won": team["roundsWon"],
                } for team in match_data["teams"]
            ],
            "players": [
                [
                    {
                        "puuid": player["subject"],
                        "display_name": player["gameName"],
                        "team_id": player["teamId"],
                        "agent_id": player["characterId"],
                        "agent_display_name": [agent for agent in content["agents"] if player["characterId"] in agent["uuid"]][0]["display_name"],
                        "kd": str(round(player["stats"]["kills"] / player["stats"]["deaths"],1)),
                        "kills": player["stats"]["kills"],
                        "combat_score": player["stats"]["score"] // total_rounds,
                    } for player in match_data["players"] if player["teamId"] == team["teamId"]
                ] for team in match_data["teams"]
            ],
        }
        
        # sort players by combat score
        payload["players"] = [sorted(team, key=lambda k: k["combat_score"], reverse=True) for team in payload["players"]]

        # sort teams by red/blue
        backup = payload["teams"].copy()
        team_blue = [team for team in backup if team["team_name"] == "Blue"]
        team_red = [team for team in backup if team["team_name"] == "Red"]
        payload["teams"] = [team_red[0],team_blue[0]]

        #print(payload)
        return payload