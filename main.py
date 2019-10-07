import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import sys
import re
import urllib.request
import os
import tqdm

os.makedirs("dataset", exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}

url = sys.argv[1]
if "spacetelescope.org" not in url:
        print("\n\turl is not spacetelescope. exiting...")
        sys.exit(-1)

if url[-1] != '/':
        url += '/'

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, "lxml")
pages = []
for a in soup.findAll('a', href=True):
    if "/page/" in a['href']:
        pages.append(int(a['href'].split("/")[-2]))

tags = []
print("Fetching image ids")
for p in tqdm.tqdm(range(min(pages), max(pages)+1)):
    response = requests.get(f"{url}page/{p}/", headers=headers)
    for match in re.findall("images/thumb300y/(\w+).jpg", response.content.decode()):
        tags.append(match)

print("Downloading images")
for tag in tqdm.tqdm(tags):
    urllib.request.urlretrieve(f"https://cdn.spacetelescope.org/archives/images/large/{tag}.jpg",
        f"dataset/{tag}.jpg")
