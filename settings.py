SETTINGS = {
	"agent": "Mozilla/5.0 (compatible; Quick-Python-Crawler/0.1; +https://github.com/sedthh/quick-crawler-hun)",
	"sites": "url.csv",
	"output": "jobs.csv",
	"depth": 2,
	"sleep": .25,
	"timeout": 3,
	"exclude": ["google.com", "youtube.com", "facebook.com", "twitter.com"],
	"ignore": ["pdf", "jpg", "jpeg", "png", "gif", "swf"],
	"log_level": 0
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
	".NET": [{"stem": "(ASP)?\s?\.NET", "wordclass": "regex", "ignorecase": False}],
	"tester": [{"stem": "tesz?t(el[oöő]|\s?automat\w+|\s?engin\w+)", "wordclass": "regex"}],
	"embedded": [{"stem": "embedded"},{"stem": "beágyazott"}],
	"Selenium": [{"stem": "Selenium", "wordclass": "noun"}],
	"AWS": [{"stem": "AWS", "ignorecase": False}],
	"Azure": [{"stem": "Azure", "wordclass": "noun"}],
	"DevOps": [{"stem": "Dev Ops"}],
	"Data Science": [{"stem":"data\s?(scien|engin)\w+", "wordclass": "regex"}],
	"React": [{"stem": "React", "wordclass": "noun"}],
	"Android": [{"stem": "Android", "wordclass": "noun"}],
	"OpenCV": [{"stem": "Open CV"}],
	"fullstack": [{"stem": "full stack"}],
	"frontend": [{"stem": "front end"}],
	"backend": [{"stem": "back end"}],
	"SQL": [{"stem": "SQL", "prefix":["My"]}],
	"docker": [{"stem": "Docker", "wordclass": "noun"}]
}
