from websitesearch import *
import argparse
from pathlib import Path
import concurrent.futures
with open("data.json") as data:
    websites_json = json.load(data)

parser = argparse.ArgumentParser(description="Get socials and save it to a text file")
parser.add_argument("username", type=str, help="Input username of person")
parser.add_argument("-fo", "--folderoutput", type=str, help="Specify directory for text files to be saved")
parser.add_argument("-o", "--output", type=str, help="Specify text file to be overwritten with this data")
args = parser.parse_args()

def main():
    print("start")
    def check(website):
        search = WebsiteSearch(website, args.username)
        if search.is_valid():
            download_path = Path("downloads/") / f"{args.username}.txt"
            if args.folderoutput:
                download_path = Path(args.folderoutput) / f"{args.username}.txt"
            if args.output:
                download_path = Path(args.output)
            with open(download_path, "a") as website_write:
                website_write.write(f"{search.url}\n")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for website in websites_json:
            executor.submit(check, website)

if __name__ ==  "__main__":            
    main()