from BeautifulSoup import BeautifulSoup as Soup
import re
import urllib

if len(sys.argv) != 2:
	sys.exit(1)

word = sys.argv[1]
url = "http://en.wikipedia.org/wiki/" + word
page = Soup(urllib.urlopen(url))

