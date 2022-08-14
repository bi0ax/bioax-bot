import requests
import json
import statistics
from line_profiler import LineProfiler
import concurrent.futures
api_key = "466218a2-265f-4662-8fff-7618d8d31178"
headers = {"accept":"application/json", "Authorization": "Bearer {}".format(api_key)}
class FaceitUser:
    def __init__(self, username=None):
        self.players_url = "https://open.faceit.com/data/v4/players"
        self.matches_url = "https://open.faceit.com/data/v4/matches"
        self.valid = True
        self.player_id = ""
        self.player_json = {}
        self.player_response = requests.get(f"{self.players_url}?nickname={username}", headers=headers)
        if self.player_response.status_code != 200:
            self.valid = False
        else:
            self.player_json = json.loads(self.player_response.text)
            self.player_id = self.player_json["player_id"]

    def get_matches(self, matches=20): # returns a list of match id's
        self.response_matches = requests.get(f"{self.players_url}/{self.player_id}/history?game=csgo&offset=0&limit={matches}", headers=headers)
        if self.response_matches.status_code != 200:
            return "Error"
        self.matches = json.loads(self.response_matches.text)
        return [x["match_id"] for x in self.matches["items"]]
    def get_stats(self, count=20):
        self.user_stats = []
        def get_match_stats():
            self.response_match_stats = requests.get(f"{self.matches_url}/{x}/stats", headers=headers)
            self.match_stats = json.loads(self.response_match_stats.text)
            self.match_rounds = self.match_stats["rounds"]
            self.match_teams = self.match_rounds[0]["teams"] # BO1 most of time
            self.match_team_stats_added = self.match_teams[0]["players"] + self.match_teams[1]["players"] #list of players, which has a key inside each dict
            self.user_stats_temp = [(y["player_stats"]["K/D Ratio"], y["player_stats"]["K/R Ratio"]) for y in self.match_team_stats_added if y["player_id"] == self.player_id]
            #each element above is (K/D, K/R)
            self.user_stats.extend(self.user_stats_temp)
        with concurrent.futures.ThreadPoolExecutor() as executor:    
            for x in self.get_matches(count):
                executor.submit(get_match_stats)
            
        return self.user_stats
    def get_KD(self,stats): #stats must be dict from get_stats()
        return statistics.mean([float(x[0]) for x in stats])
    def get_KR(self,stats):
        return statistics.mean([float(x[1]) for x in stats])
    
    def get_lifetime_stats(self):
        self.lifetime_stats_response = requests.get(f"{self.players_url}/{self.player_id}/stats/csgo", headers=headers)
        self.lifetime_stats = json.loads(self.lifetime_stats_response.text)
        return self.lifetime_stats
    def get_lifetime_overall(self): 
        gls = self.get_lifetime_stats()
        return gls["lifetime"] if gls != "Error" else None
    def get_best_map(self): 
        gls = self.get_lifetime_stats()
        self.best_maps = sorted(gls["segments"], key=lambda x: float(x["stats"]["Average K/D Ratio"]), reverse=True)
        return self.best_maps[0] if gls != "Error" else None

f = FaceitUser("bi0ax")
print(f.get_stats())