from src import valorant_manager
from src import image_builder

import traceback
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from InquirerPy import inquirer

def loop():
    
    mgr = valorant_manager.Valorant()
    content = mgr.content
    while True:
        print("fetching recent matches")
        matches = mgr.client.fetch_match_history()["History"]
        choices = [Choice("custom","use my own match id"),Separator()]
        for match in matches:
            match_data = mgr.client.fetch_match_details(match["MatchID"])

            me = next(player for player in match_data["players"] if player["subject"] == mgr.client.puuid)
            my_team = next(team for team in match_data["teams"] if team["teamId"] == me["teamId"])
            other_team = next(team for team in match_data["teams"] if team["teamId"] != me["teamId"])

            queue = match_data["matchInfo"]["queueID"]
            if queue == " " or queue == "":
                queue = "custom"
            match_id = match_data["matchInfo"]["matchId"]
            score = f"{my_team['roundsWon']}-{other_team['roundsWon']}"

            agent = next(agent for agent in content["agents"] if agent["uuid"] == me["characterId"])
            agent = agent["display_name"]

            string = f"[{score}] {queue} - {agent} ({match_id})"
            choices.append(Choice(match_id, string))

        match_id = inquirer.select("pick a match", choices).execute()
        if match_id == "custom":
            match_id = inquirer.text("enter match id").execute()
        
        if match_id is not None and match_id != "":
            try:
                print("generating image")
                data = mgr.load_match_data(match_id)
                builder = image_builder.Builder(data)
                builder.build_image()
                print("done")
            except:
                traceback.print_exc()
        

if __name__ == "__main__":

    loop()

    # builder = image_builder.Builder(data)
    # builder.build_image()
    # print("done")