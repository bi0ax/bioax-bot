import requests
import datetime
import json
import statistics
class Item: 
    def __init__(self, name): #name must be a tuple
        self.url_name = ("_".join(name.split())).lower()
        self.response = requests.get("https://api.warframe.market/v1/items/{}/orders".format(self.url_name))
        temp = requests.get("https://api.warframe.market/v1/items/{}/orders".format(self.url_name + "_blueprint"))
        if self.response.status_code != 200 and temp.status_code == 200:
            self.response = temp
        self.item = json.loads(self.response.text) 
    def get_plat(self):
        if self.response.status_code != 200:
            return "Error"
        sales = []
        self.item_orders = self.item["payload"]["orders"]
        new = [x["platinum"] for x in self.item_orders if x["order_type"] == "sell"]
        return statistics.median(new)
