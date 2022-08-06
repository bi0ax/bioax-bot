import requests
import datetime
import json
import statistics
class Item: 
    def __init__(self, name): #name must be a tuple
        self.url_name = ("_".join(name.split())).lower()
        self.market_response = requests.get("https://api.warframe.market/v1/items/{}/orders".format(self.url_name))
        temp = requests.get("https://api.warframe.market/v1/items/{}/orders".format(self.url_name + "_blueprint"))
        if self.market_response.status_code != 200 and temp.status_code == 200:
            self.market_response = temp
        self.orders = json.loads(self.market_response.text) 
    def get_plat(self):
        if self.market_response.status_code != 200:
            return "Error"
        self.item_orders = self.orders["payload"]["orders"]
        plat_prices = [x["platinum"] for x in self.item_orders if x["order_type"] == "sell"]
        return statistics.median(plat_prices)
