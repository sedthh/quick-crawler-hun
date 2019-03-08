# Simple webspider for crawling sites in Hungarian
A basic Python crawler based on the [Hungarian NLP library, Lara](https://github.com/sedthh/lara-hungarian-nlp) that visits URLs and checks if a predefined set of keywords (ore their inflected forms) are present on these sites in Hungarian.

**Ez egy egyszerű, magyarnyelvű webcrawler, ami ragozott formájú kulcsszavak meglétének vizsgálatára készült.**

The following example searches for topics about *Brexit* on the given list of sites (the crawler will also follow links that have words like "külföldön", "kulfold", "gazdasági", "gazdasagos", "politikáról", "politikai", etc. in them either in the href=URL slug, or in between the \<a\>tags\<\/a\>):

This example checks articles on *index.hu* and *hvg.hu*:

```python
from spider import QuickCrawler

match_sites = {
	"kulfold": [{"stem": "külföld", "wordclass": "noun"}],
	"gazdasag": [{"stem": "gazdaság", "wordclass": "noun"}],
	"politika": [{"stem": "politika", "wordclass": "noun"}],
}

match_keywords = {
	"anglia": [{"stem": "Anglia", "wordclass": "noun"},
                {"stem": "London", "wordclass": "noun"},
                {"stem": "brit", "wordclass": "adjective"}],
	"brexit": [{"stem": "Brexit", "wordclass": "noun"}]
}

if __name__ == "__main__":
	spider = QuickCrawler({"depth": 2}, match_keywords, match_sites)
	sites = ["www.index.hu", "www.hvg.hu"]
	for url, value in spider.crawl(sites):
		print(url, ', '.join(value))
```
