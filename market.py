import requests
import datetime
import json
import statistics
class Item: 
    def __init__(self, item_name): #name must be a tuple
        self.valid = True
        self.url_name = ("_".join(item_name.split())).lower()
        self.market_response = requests.get("https://api.warframe.market/v1/items/{}/orders".format(self.url_name))
        temp = requests.get("https://api.warframe.market/v1/items/{}/orders".format(self.url_name + "_blueprint"))
        if self.market_response.status_code != 200 and temp.status_code == 200:
            self.market_response = temp
        elif self.market_response.status_code != 200 and temp.status_code != 200:
            self.valid = False
        self.orders = json.loads(self.market_response.text) 
    def get_plat(self):
        self.orders_list = self.orders["payload"]["orders"]
        plat_prices = [x["platinum"] for x in self.orders_list if x["order_type"] == "sell"]
        return statistics.median(plat_prices)
