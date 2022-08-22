import requests
import datetime
import json
import time
from pathlib import Path
from bs4 import BeautifulSoup
from market import *
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
        self.valid = True
        if self.response.status_code != 200:
            self.valid = False
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
        if datetime.datetime.now() > datetime.datetime.fromisoformat(self.get_challenge_expiry(index)):
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

class Weapon:
    def __init__(self, weapon_name):
        weapon_data_path = Path("botinfo/warframedata/weapon_data.txt")
        weapon_data_read = open(weapon_data_path, "r")
        self.all_weapon_data = json.loads(weapon_data_read.read())
        self.weapon_stats = [weapon for weapon in self.all_weapon_data if weapon["name"] == weapon_name.title()][0]
        self.weapon_attacks = self.weapon_stats["attacks"]
    
class Warframe:
    def __init__(self, warframe_name):
        self.warframe_name = warframe_name
        warframe_data_path = Path("botinfo/warframedata/warframe_data.txt")
        warframe_data_read = open(warframe_data_path, "r")
        self.all_warframe_data = json.loads(warframe_data_read.read())

class Mods:
    def __init__(self):
        mod_data_path = Path("botinfo/warframedata/mod_data.txt")
        warframe_data_read = open(mod_data_path, "r")
        self.all_mod_data = json.load(warframe_data_read)
        self.all_augments = [x for x in self.all_mod_data if "isAugment" in x.keys() and x["isAugment"] == True]
        self.all_primed = [x for x in self.all_mod_data if x['name'].startswith("Primed")]

class Mod:
    def __init__(self, mod_name):
        self.mod_name = mod_name
        mod_data_path = Path("botinfo/warframedata/mod_data.txt")
        warframe_data_read = open(mod_data_path, "r")
        self.all_mod_data = json.load(warframe_data_read)
        self.mod = [x for x in self.all_mod_data if x["name"] == mod_name.title()][0]

class ItemDrop:
    def __init__(self, item_name):
        self.item_name = item_name
        self.formatted_item_name = self.item_name.replace(" ", "%20")
        item_drop_response = requests.get(f"https://api.warframestat.us/drops/search/{self.formatted_item_name}")
        self.item_drops = json.loads(item_drop_response.text)
        self.item_found = True
        if not self.item_drops:
            self.item_found = False

class Items:
    def __init__(self):
        item_data_path = Path("botinfo/warframedata/item_data.txt")
        item_data_read = open(item_data_path, "r")
        self.all_item_data = json.load(item_data_read)
        self.all_ayatan = [x for x in self.all_item_data if x["name"].startswith("Ayatan")]
        self.ayatan_prices = json.load(open(Path("botinfo/warframedata/ayatan_data.txt"), "r"))
