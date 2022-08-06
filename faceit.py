import requests
import json
import statistics
from line_profiler import LineProfiler
api_key = "466218a2-265f-4662-8fff-7618d8d31178"
headers = {"accept":"application/json", "Authorization": "Bearer {}".format(api_key)}
class FaceitUser:
    def __init__(self, username=None):
        self.players_url = "https://open.faceit.com/data/v4/players"
        self.matches_url = "https://open.faceit.com/data/v4/matches"
        self.response_for_id = requests.get(f"{self.players_url}?nickname={username}", headers=headers)
        self.player_id = json.loads(self.response_for_id.text)["player_id"]
    def get_matches(self, matches=5): # returns a list of match id's
        self.response_matches = requests.get(f"{self.players_url}/{self.player_id}/history?game=csgo&offset=0&limit={matches}", headers=headers)
        if self.response_matches.status_code != 200:
            return "Error"
        self.matches = json.loads(self.response_matches.text)
        return [x["match_id"] for x in self.matches["items"]]

    def get_stats(self, count=5):
        self.user_stats = []
        for x in self.get_matches(count):
            self.response_match_stats = requests.get(f"{self.matches_url}/{x}/stats", headers=headers)
            self.match_stats = json.loads(self.response_match_stats.text)
            self.match_rounds = self.match_stats["rounds"]
            self.match_teams = self.match_rounds[0]["teams"] # BO1 most of time
            self.match_team_stats_added = self.match_teams[0]["players"] + self.match_teams[1]["players"] #list of players, which has a key inside each dict
            self.user_stats_temp = [(y["player_stats"]["K/D Ratio"], y["player_stats"]["K/R Ratio"]) for y in self.match_team_stats_added if y["player_id"] == self.player_id]
            #each element above is (K/D, K/R)
            self.user_stats.extend(self.user_stats_temp)    
        return self.user_stats
    def get_KD(self,stats):
        return statistics.mean([float(x[0]) for x in stats])
    def get_KR(self,stats):
        return statistics.mean([float(x[1]) for x in stats])
f = FaceitUser("1gnomeo")
stats = f.get_stats(20)
print(f.player_id)