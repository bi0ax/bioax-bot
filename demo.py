from awpy.parser import DemoParser
from awpy.analytics.stats import player_stats
class Demo:
    def __init__(self, file):
        demo_parser = DemoParser(demofile=file, parse_rate=128)
        self.demo = demo_parser.parse()
        self.player_stats = player_stats(self.demo["gameRounds"])
        self.steam_ids = [x.split(" ")[0] for x in self.player_stats]
            
    def id(self, id): #takes in either steam community id or case sensitive username
        a = list(filter(lambda x: str(id) in x, self.player_stats.keys()))
        return a[0] if a else "Error"
    
    def get_stats(self, player): #player must be self.id() function 
        return self.player_stats[player] if player != "Error" else "Player not found"

d = Demo("demoes\\liquid-vs-evil-geniuses-m4-mirage.dem")
#d2 = Demo("demoes\\inferno_1v4ninja.dem")
brehze = d.id("Brehze")
print(d.get_stats(brehze))
#print(d2.get_stats(d2.id("bi0ax")))