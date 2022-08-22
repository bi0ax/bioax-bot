import requests
import datetime
import json
import statistics
class OldMarketItem: 
    def __init__(self, item_name): #name must be a tuple
        self.item_name = item_name
        self.valid = True
        self.url_name = ("_".join(item_name.split())).lower()
        self.market_response = requests.get("https://api.warframe.market/v1/items/{}/orders".format(self.url_name))
        temp = requests.get("https://api.warframe.market/v1/items/{}/orders".format(self.url_name + "_blueprint"))
        if self.market_response.status_code != 200 and temp.status_code == 200:
            self.market_response = temp
        elif self.market_response.status_code != 200 and temp.status_code != 200:
            self.valid = False
        self.status_code = self.market_response.status_code
        self.orders = json.loads(self.market_response.text) if self.valid == True else None
    def get_plat(self):
        if not self.orders:
            print(self.item_name + str(self.status_code))
            return 0
        self.orders_list = self.orders["payload"]["orders"]
        plat_prices = [x["platinum"] for x in self.orders_list if x["order_type"] == "sell"]
        return statistics.median(plat_prices)

class MarketItem:
    def __init__(self, item_name):
        self.item_name = item_name
        self.valid = True
        self.url_name = ("_".join(item_name.split())).lower()
        self.market_response = requests.get(f"https://api.warframe.market/v1/items/{self.url_name}/statistics")
        temp = requests.get("https://api.warframe.market/v1/items/{}/statistics".format(self.url_name + "_blueprint"))
        if self.market_response.status_code != 200 and temp.status_code == 200:
            self.market_response = temp
        elif self.market_response.status_code != 200 and temp.status_code != 200:
            self.valid = False
        self.statistics = json.loads(self.market_response.text) if self.valid else None
        self.yesterday_stats = self.statistics["payload"]["statistics_closed"]["90days"][-1] if self.statistics else None
        self.ninety_day_stats = self.statistsics["payload"]["statistics_closed"]["90days"] if self.statistics else None
        self.plat = self.yesterday_stats["median"] if self.statistics else 0
        self.volume = self.yesterday_stats["volume"] if self.statistics else 0
    def get_plat(self):
        if not self.statistics:
            return 0
        return self.plat
    def get_volume_avg(self, days):
        if not self.statistics:
            return 0
        volumes = [int(self.ninety_day_stats[x]["volume"]) for x in range(-1, days*-1, -1)] 
        return statistics.mean(volumes)            




