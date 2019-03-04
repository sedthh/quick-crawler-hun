import os
import re
import pandas as pd
import time
from datetime import datetime
from settings import SETTINGS, URL_MATCH, TEXT_MATCH
from spider import QuickCrawler


def get_site_list(csv):
	file = os.path.join(os.path.dirname(os.path.realpath(__file__)), csv)
	df = pd.read_csv(file, sep=";")
	sites = []
	for index, row in df.iterrows():
		url = str(row["url"]).strip()
		if url == "nan":
			continue
		if not re.findall(r'^https?\:\/\/\S+', url, re.IGNORECASE):
			url = "http://"+url
		url = url.split()[0]
		if url not in sites:
			sites.append(url)
	return sites


def save(file, url, info):
	file = os.path.join(os.path.dirname(os.path.realpath(__file__)), file)
	data = {"time": [datetime.now().strftime("%Y-%m-%d")], "url": [url], "info": [info]}
	df = pd.DataFrame(data, columns=data.keys())
	df.to_csv(file, mode='a', header=False, index=False, sep=";")


if __name__ == "__main__":
	start = time.time()
	spider = QuickCrawler(SETTINGS, TEXT_MATCH, URL_MATCH)
	sites = get_site_list(SETTINGS["sites"])
	for url, value in spider.crawl(sites):
		save(SETTINGS["output"], url, " ".join(value))
	end = time.time()
	print(f"Crawler finished in {end-start} seconds.")

