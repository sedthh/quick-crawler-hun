import sys
import os
import requests
import bs4
import re
import time
from datetime import datetime
from urllib.parse import urlsplit

try:
	import lara
except ImportError as error:
	sys.path.append(os.path.join(os.pardir, "lara-hungarian-nlp"))
	import lara


class QuickCrawler:

	def __init__(self, settings={}, text_intents={}, url_intents={}):
		self._agent = settings.get("agent",
								   "Mozilla/5.0 (compatible; Quick-Python-Crawler/0.1; +https://github.com/sedthh/quick-crawler-hun)")
		self._depth = settings.get("depth", 2)
		self._sleep = settings.get("sleep", .25)
		self._timeout = settings.get("timeout", 3)
		self._exclude = settings.get("exclude", ["google.com", "youtube.com", "facebook.com", "twitter.com"])
		self._ignore = settings.get("ignore", [])
		self._log_level = settings.get("log_level", 0)

		self.visited = []
		self.url_intents = lara.parser.Intents(url_intents)
		self.text_intents = lara.parser.Intents(text_intents)

	def __repr__(self):
		return "<Quick Crawler instance at {0}>".format(hex(id(self)))

	def __str__(self):
		return ', '.join(self.visited)

	def __len__(self):
		return len(self.visited)

	def _tag_visible(self, element):
		if element.parent.name in ("style", "script", "head", "title", "meta", "[document]"):
			return False
		if isinstance(element, bs4.Comment):
			return False
		return True

	def _match_links(self, soup):
		hrefs = []
		for href in soup.findAll("a"):
			if self.url_intents.match_set(href.get("href")):
				hrefs.append(href.get("href"))
			if href.string:
				if self.url_intents.match_set(href.string):
					hrefs.append(href.get("href"))
		return set(hrefs)

	def _match_text(self, soup):
		# via https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
		texts = soup.findAll(text=True)
		visible_texts = filter(self._tag_visible, texts)
		text = " ".join(t.strip() for t in visible_texts if t.strip())
		return self.text_intents.match_set(text)

	def _get_plain_url(self, url):
		if url:
			url = url.split("#")[0].split("?")[0]
			if url[-1] in ("\\", "/"):
				return ''.join(url[:-1])
		return url

	def log(self, info, level=0):
		if level >= self._log_level:
			now = datetime.now().strftime("%H:%M:%S")
			print(f"{now} > " + info, flush=True)

	def flush(self):
		self.visited = []

	def crawl(self, urls):
		for url in urls:
			if not re.findall(r'^https?\:\/\/\S+', url, re.IGNORECASE):
				url = "http://" + url
			url = url.split()[0]
			results = self._crawl_url(url, self._depth)
			if results:
				for key, value in results.items():
					if value:
						yield key, value

	def _crawl_url(self, url, depth):
		if not url:
			return {}
		for format in self._ignore:
			if url.endswith("." + format):
				self.log(f"WARNING: format for {url} is not allowed", 1)
				return {}
		plain_url = self._get_plain_url(url)
		if plain_url in self._exclude:
			self.log(f"WARNING: {url} is in the exclude list", 1)
			return {}
		if plain_url in self.visited:
			self.log(f"WARNING: already visited {plain_url}", 1)
			return {}
		self.visited.append(plain_url)
		self.log(f"Crawling: {url}")
		try:
			data = requests.get(url, timeout=self._timeout, headers={"User-Agent": self._agent})
		except requests.exceptions.Timeout:
			self.log(f"ERROR: server timeout for {url}", 2)
			return {}
		except requests.exceptions.TooManyRedirects:
			self.log(f"ERROR: too many redirects for {url}", 2)
			return {}
		except requests.exceptions.ConnectionError:
			self.log(f"ERROR: could not connect {url}", 2)
			return {}
		except requests.exceptions.MissingSchema:
			self.log(f"ERROR: invalid url {url}", 2)
			return {}
		except requests.exceptions.InvalidSchema:
			self.log(f"ERROR: invalid url {url}", 2)
			return {}
		except requests.exceptions.HTTPError as err:
			self.log(f"ERROR: {url} returned with HTTP error {err}", 2)
			return {}

		soup = bs4.BeautifulSoup(data.text, "lxml")
		results = {url: self._match_text(soup)}
		if depth > 0:
			links = self._match_links(soup)
			if links:
				self.log(f"Found {len(links)} link(s)")
				for link in links:
					if link and "@" not in link:
						time.sleep(self._sleep)
						if not re.findall(r'^https?\:\/\/\S+', link, re.IGNORECASE):
							if link not in url:
								domain = "{0.scheme}://{0.netloc}/".format(urlsplit(url))
								if domain not in link:
									if link[0] in ("\\", "/") and domain[-1] in ("\\", "/"):
										link = domain + ''.join(link[1:])
									else:
										link = domain + link
						subdomain = self._crawl_url(link, depth - 1)
						if subdomain:
							for key, value in subdomain.items():
								if value:
									results[key] = value

		return results
