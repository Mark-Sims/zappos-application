from urllib2 import Request, urlopen, URLError

request = Request('http://api.zappos.com/Search?term=boots&key=52ddafbe3ee659bad97fcce7c53592916a6bfd73')

try:
	response = urlopen(request)
	kittens = response.read()
	print kittens[559:1000]
except URLError, e:
    print 'No kittez. Got an error code:', e