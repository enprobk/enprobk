import urllib2

url = 'http://203.247.39.98/'

try:
	data = urllib2.urlopen(url).read()
except urllib2.HTTPError, e:
	print "HTTP error : %d" % e.code
except urllib2.URLError, e:
	print "Network Error: %s" % e.reason.args[1]

	

"""
u = urllib.urlopen(url)
data = u.read()
"""

