# -*- coding: utf-8 -*-
# enprobk@

import urllib2, sys, argparse, hashlib

reload(sys)
sys.setdefaultencoding('utf-8')

class MACA_API():
	#url = 'http://203.247.39.98'

	def __init__(self, sha):
		self.url = 'http://203.247.39.98/maca_api'
		self.sha = sha

	def get_data(self):
		try:
			self.data = urllib2.urlopen(self.url).read()
		except urllib2.HTTPError, e:
			print "HTTP error : %d" % e.code
		except urllib2.URLError, e:
			print "Network Error: %s" % e.reason.args[1]

		#print self.data

	def print_data(self):
		print self.data

def main():
	opt=argparse.ArgumentParser(description="Search and Download from MACA")
	opt.add_argument("HashorPath", help="Enter the SHA Hash or Path to File")
	#opt.add_argument("-u", "--url", action="store_true", help="Search VirusTotal")

	if len(sys.argv)<2:
		opt.print_help()
		sys.exit(1)

	options = opt.parse_args()
	sha = options.HashorPath
	print sha
	maca = MACA_API(sha)
	
	maca.get_data()
	maca.print_data()	

if __name__ == "__main__":
	

	try:
		main()
	except Exception as e:
		print e.message

