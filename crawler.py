import sys
import os
import pandas as pd
import requests
import bs4
import re
import time
from datetime import datetime
from urllib.parse import urlparse

try:
	import lara
except ImportError as error:
	sys.path.append(os.path.join(os.pardir, "lara-hungarian-nlp"))
	import lara

SETTINGS = {
	"agent": "Mozilla/5.0 (compatible; Quick-Python-Crawler/0.1; +https://github.com/sedthh/quick-crawler-hun)",
	"sites": "url.csv",
	"output": "jobs.csv",
	"depth": 2,
	"sleep": .25,
	"timeout": 3,
	"exclude": ["google.com", "youtube.com", "facebook.com", "twitter.com"]
}

URL_MATCH = {
	"job": [{"stem": "munka", "wordclass": "noun", "affix": ["lehetőség", "keres", "társ"]},
			{"stem": "állás", "wordclass": "noun", "affix": ["lehetőség", "keres", "hírdetés", "ajánlat"]},
			{"stem": "karrier", "wordclass": "noun", "affix": ["lehetőség", "keres", "portál"]},
			{"stem": "pozíció", "wordclass": "noun"},
			{"stem": "gyakornok", "wordclass": "noun"},
			{"stem": "dolgoz", "wordcloass": "verb", "prefix": []},
			{"stem": "csatlakoz", "wordclass": "verb", "prefix": []},
			{"stem": "(job(s|\s?op+ortuni\w+)|care+rs?|hiring|work(ing)?|recruit(ment|ing)?|join|openings?|positions?)", "wordclass": "regex"}]
}

TEXT_MATCH = {
	"PHP": [{"stem": "PHP", "wordclass": "noun"}],
	"JAVA": [{"stem": "JAVA", "wordclass": "noun"}],
	"JavaScript": [{"stem": "Java Script", "wordclass": "noun"}],
	"Spring": [{"stem": "Spring", "wordclass": "noun"}],
	"Angular": [{"stem": "Angular", "wordclass": "noun"}],
	"Python": [{"stem": "Python", "wordclass": "noun"}],
	"C": [{"stem": "C", "ignorecase": False}],
	"C++": [{"stem": "C\s?\+\+", "wordclass": "regex", "ignorecase": False}],
	"C#": [{"stem": "C#", "wordclass": "regex", "ignorecase": False}],
	"TS": [{"stem": "Type Script", "wordclass": "noun"}],
	".NET": [{"stem": ".NET", "ignorecase": False}],
	"tester": [{"stem": "tesz?t(el[oöő]|\s?automat\w+)", "wordclass": "regex"}],
	"embedded": [{"stem": "embedded"},{"stem": "beágyazott"}],
	"Selenium": [{"stem": "Selenium", "wordclass": "noun"}],
	"AWS": [{"stem": "AWS", "ignorecase": False}],
	"Azure": [{"stem": "Azure", "wordclass": "noun"}],
	"DevOps": [{"stem": "Dev Ops"}],
	"Data Science": [{"stem":"data\s?(scien|engin)\w+", "wordclass": "regex"}]
}

def get_sites(csv):
	file = os.path.join(os.path.dirname(os.path.realpath(__file__)), csv)
	df = pd.read_csv(file, sep=";")
	for index, row in df.iterrows():
		url = str(row["url"]).strip()
		if url == "nan":
			continue
		if not re.findall(r'^https?\:\/\/\S+', url, re.IGNORECASE):
			url = "http://"+url
		yield url.split()[0]


def tag_visible(element):
	if element.parent.name in ("style", "script", "head", "title", "meta", "[document]"):
		return False
	if isinstance(element, bs4.Comment):
		return False
	return True


def crawl(url, depth=3):
	global SETTINGS
	if pretty_url(url) in SETTINGS["exclude"]:
		return
	SETTINGS["exclude"].append(pretty_url(url))
	log(f"Crawling: {url}")
	depth -= 1
	try:
		data = requests.get(url, timeout=SETTINGS["timeout"], headers={"User-Agent": SETTINGS["agent"]})
	except requests.exceptions.Timeout:
		log(f"ERROR: server timeout")
		return
	except requests.exceptions.TooManyRedirects:
		log(f"ERROR: too many redirects")
		return
	except requests.exceptions.ConnectionError:
		log(f"ERROR: could not connect")
		return
	except requests.exceptions.MissingSchema:
		log(f"ERROR: invalid url {url}")
		return
	except requests.exceptions.InvalidSchema:
		log(f"ERROR: invalid url {url}")
		return
	except requests.exceptions.HTTPError as err:
		log(f"ERROR: HTTP error {err}")
		return

	soup = bs4.BeautifulSoup(data.text, "lxml")
	results = {url: match_text(soup)}
	if depth > 0:
		links = match_links(soup)
		if links:
			log(f"Found {len(links)} link(s)")
			for link in links:
				if link and "@" not in link:
					time.sleep(SETTINGS["sleep"])
					if not re.findall(r'^https?\:\/\/\S+', link, re.IGNORECASE):
						if link not in url:
							link = url + link
					subdomain = crawl(link, depth)
					if subdomain:
						for key, value in subdomain.items():
							if value:
								#log(f"Position: {value}")
								results[key] = value

	return results


def match_links(soup):
	links = []
	match = lara.parser.Intents(URL_MATCH)
	for link in soup.findAll("a"):
		if match.match_set(link.get("href")):
			links.append(link.get("href"))
		if link.string:
			if match.match_set(link.string):
				links.append(link.get("href"))
	return set(links)


def match_text(soup):
	# via https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
	texts = soup.findAll(text=True)
	visible_texts = filter(tag_visible, texts)
	text = " ".join(t.strip() for t in visible_texts if t.strip())
	return lara.parser.Intents(TEXT_MATCH).match_set(text)


def pretty_url(url):
	o = urlparse(url)
	return "/".join([o.netloc, o.path])


def log(info):
	now = datetime.now().strftime("%H:%M:%S")
	print(f"{now} > "+info, flush=True)


def save(file, url, info):
	log(f"Saving results for {url}: {info}")
	file = os.path.join(os.path.dirname(os.path.realpath(__file__)), file)
	data = {"time": [datetime.now().strftime("%Y-%m-%d")], "url": [url], "info": [info]}
	df = pd.DataFrame(data, columns=data.keys())
	df.to_csv(file, mode='a', header=False, index=False, sep=";")

if __name__ == "__main__":
	for site in get_sites(SETTINGS["sites"]):
		result = crawl(site, SETTINGS["depth"])
		if result:
			for key, value in result.items():
				if value:
					save(SETTINGS["output"], key, " ".join(value))


