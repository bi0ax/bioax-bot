import requests, json
from pathlib import Path
import concurrent.futures
with open("socialpuller/data.json") as data:
    websites_json = json.load(data)

class WebsiteSearch:
    def __init__(self, website, username):    
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
        }
        self.website_data = websites_json.get(website)
        if "headers" in self.website_data:
            self.headers = self.website_data["headers"]
        self.url = self.website_data["url"].format(username)
        self.response = requests.get(self.url, headers=self.headers)
    def is_valid(self):
        self.valid_account = True
        self.error_type = self.website_data["errorType"]
        if self.error_type == "status_code": #checks for 404 or other errors
            if self.response.status_code != 200:
                self.valid_account = False
        elif self.error_type == "message": #checks if error message is on the website
            self.error_message = self.website_data["errorMsg"]
            if self.error_message in self.response.text:
                self.valid_account = False
        elif self.error_type == "response_url": #checks if there is a redirect
            if self.response.history:
                self.valid_account = False
        return self.valid_account

def search_all(username):
    def check(website):
        search = WebsiteSearch(website, username)
        if search.is_valid():
            print(f"{search.url} is VALID")
            with open(Path(f"socialpuller/downloads/{username}.txt"), "a") as website_write:
                website_write.write(f"{search.url}\n")
        else:
            print(f"{search.url} is not valid")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for website in websites_json:
            executor.submit(check, website)

search_all("bi0ax")

