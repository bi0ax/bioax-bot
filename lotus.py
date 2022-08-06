import requests
import datetime
import json
time_now = datetime.datetime.now() + datetime.timedelta(hours=4)
def is_expired(time):
        if datetime.datetime.now() > datetime.datetime.fromisoformat(time): #remember that there is Z at the end
            return True
        else:
            return False

def time_left(time):
    return datetime.datetime.fromisoformat(time) - (datetime.datetime.now()+datetime.timedelta(hours=4))

class Nightwave:
    def __init__(self):
        self.response = requests.get("https://api.warframestat.us/pc/nightwave/?language=en")
        self.current_nightwave = json.loads(self.response.text)
        self.current_nightwave_challenges = json.loads(self.response.text)["activeChallenges"]
        self.possible_nightwave_challenges = json.loads(self.response.text)["possibleChallenges"]
    def get_challenge_names(self):
        if self.response.status_code != 200:
            return "Error"
        return [x["title"] for x in self.current_nightwave_challenges]
    def get_challenge_descs(self):
        if self.response.status_code != 200:
            return "Error"
        return [x["desc"] for x in self.current_nightwave_challenges]
    def get_challenge_standings(self):
        if self.response.status_code != 200:
            return "Error"
        return [x["reputation"] for x in self.current_nightwave_challenges]
    def get_challenge_expiry(self, index):
        return self.current_nightwave_challenges[index]["expiry"][:-1]
    def get_expiry_date(self):
        return self.get_challenge_expiry().split("T")[0]
    def get_expiry_time(self):
        return self.get_challenge_expiry().split("T")[1]
    def is_expired(self, index):
        if datetime.datetime.now() > datetime.datetime.fromisoformat(nw.get_challenge_expiry(index)):
            return True
        else:
            return False
    def get_time_left(self):
        if self.response.status_code != 200:
            return "Error"
        time_lefts = []
        for x in range(0, 10):
            tl = time_left(self.get_challenge_expiry(x))
            if tl.days >= 1:
                time_lefts.append( "{}d {}h".format(tl.days, tl.days//24))
            else:
                time_lefts.append( "{}h {}m".format(tl.seconds//3600, (tl.seconds//60)%60))
        return time_lefts

class Sortie:
    def __init__(self):
        self.response = requests.get("https://api.warframestat.us/pc/sortie/?language=en")
        self.current_sortie = json.loads(self.response.text)
        self.current_sortie_missions = json.loads(self.response.text)["variants"]
    def get_mission_types(self):
        if self.response.status_code != 200:
            return "Error"
        return [x["missionType"] for x in self.current_sortie_missions]
    def get_nodes(self):
        if self.response.status_code != 200:
            return "Error"
        return [x["node"] for x in self.current_sortie_missions]
    def get_modifiers(self):
        if self.response.status_code != 200:
            return "Error"
        return [x["modifier"] for x in self.current_sortie_missions]
    def get_boss(self):
        if self.response.status_code != 200:
            return "Error"
        return self.current_sortie["boss"]

class Eidolon:
    def __init__(self):
        self.response = requests.get("https://api.warframestat.us/pc/cetusCycle/?language=en")
        self.eidolon = json.loads(self.response.text)
    def get_state(self):
        if self.response.status_code != 200:
            return "Error"
        return self.eidolon["shortString"]
    def get_day(self):
        if self.response.status_code != 200:
            return "Error"
        return "day" if self.eidolon["isDay"] else "night"

class OrbVallis:
    def __init__(self):
        self.response = requests.get("https://api.warframestat.us/pc/vallisCycle/?language=en")
        self.orb_vallis = json.loads(self.response.text)
    def get_day(self):
        if self.response.status_code != 200:
            return "Error"
        return "warm" if self.orb_vallis["isWarm"] else "cold"

class CambionDrift:
    def __init__(self):
        self.response = requests.get("https://api.warframestat.us/pc/cambionCycle/?language=en")
        self.cambion_drift = json.loads(self.response.text)
    def get_day(self):
        if self.response.status_code != 200:
            return "Error"
        return self.cambion_drift["active"]
nw = Nightwave()
sortie = Sortie()
eido = Eidolon()
