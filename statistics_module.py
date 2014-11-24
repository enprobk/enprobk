# -*- coding: utf-8 -*-
# enprobk@

import os, sys

from lurker.configuration import BaseLurkerConfig
from lurker.connection import Connection

reload(sys)
sys.setdefaultencoding('utf-8')

all_apkNum = 0
all_redNum = 0
all_orangeNum = 0
all_blueNum = 0
all_failNum = 0

class DatabaseConfig(BaseLurkerConfig):
	host = '203.247.39.98'
	user = 'maca'
	passwd = 'maca'
	db = 'maca_1021'

def GetRow_Query(query):
	connection = Connection(DatabaseConfig)
	connection.execute("set names euckr")

	try:
		row = connection.get_row(query)
		return row
	except Exception as e:
		print e.message

def count_apkNUM(site_NAME):
	query = "SELECT count(apk_id) from tbl_wait where site_name='%s'" % site_NAME
	ret = GetRow_Query(query)
	#print 'wait table - ', ret['count(apk_id)']
	count_apk = int(ret['count(apk_id)'])

	query = "SELECT count(apk_id) from tbl_analysis_result where site_name='%s'" % site_NAME
	ret = GetRow_Query(query)
	#print 'result table - ', ret['count(apk_id)']
	count_apk = count_apk + int(ret['count(apk_id)'])	
	#print 'all table - ', count_apk
	return count_apk

def count_anaNUM(site_NAME):
	query = "SELECT count(apk_id) from tbl_analysis_result where site_name='%s'" % site_NAME
	ret = GetRow_Query(query)
	#print 'result table - ', ret['count(apk_id)']
	count_apk = int(ret['count(apk_id)'])	
	#print 'all table - ', count_apk
	return count_apk

def collector_time(site_NAME):
	
	query = "SELECT down_time from tbl_analysis_result where site_name='%s' order by down_time ASC limit 1" % site_NAME
	ret = GetRow_Query(query)

	if (ret == None):
		query = "SELECT down_time from tbl_wait where site_name='%s' order by down_time ASC limit 1" % site_NAME
		ret = GetRow_Query(query)

	collec_time = str(ret['down_time'])

	query = "SELECT down_time from tbl_wait where site_name='%s' order by down_time DESC limit 1" % site_NAME
	ret = GetRow_Query(query)
	
	if (ret == None):
		query = "SELECT down_time from tbl_analysis_result where site_name='%s' order by down_time DESC limit 1" % site_NAME
		ret = GetRow_Query(query)

	collec_time = collec_time + ' ~ ' + str(ret['down_time'])

	#print collec_time
	return collec_time

	#count_apk = int(ret['count(apk_id)'])

def get_riskResult(site_NAME, risk):
	query = "SELECT count(apk_id) from tbl_analysis_result where total_risk='%s' and site_name='%s'" % (risk ,site_NAME)
	ret = GetRow_Query(query)

	return ret['count(apk_id)']


def collector_statistics(site_NAME):
	global all_apkNum, all_redNum, all_orangeNum, all_blueNum, all_failNum

	apkNum = count_apkNUM(site_NAME)
	anaNum = count_anaNUM(site_NAME)
	collect_time = collector_time(site_NAME)
	risk1 = get_riskResult(site_NAME, 'red')
	risk2 = get_riskResult(site_NAME, 'orange')
	risk3 = get_riskResult(site_NAME, 'blue')
	risk4 = get_riskResult(site_NAME, ' ')
	
	
	print 'collector Statistics'
	print '   [ ', site_NAME, ' ]'

	print '  1) Statistics infomation'
	print '	Time 			: ( ', collect_time, ' )'
	print '	collect_Num 		: ( ', apkNum ,' )'
	print '	Analysis_Num 		: ( ', anaNum ,' )'
	print '  2) Risk Statistics'
	print '	RED 	 : ( ', risk1 ,' )'
	print '	ORANGE 	 : ( ', risk2 ,' )'
	print '	BLUE 	 : ( ', risk3 ,' )'
	print '	Fail 	 : ( ', risk4 ,' )'
	
	#print 'SiteName \t CollectTime \t\t CollectNum \t AnalysisNum \t RED \t ORANGE \t BLUE \t Fail \t'
	"""
	print '  %s \t  %s  \t\t  %s    \t %s    \t  %s \t   %s   \t  %s  \t  %s  \t' % \
			(site_NAME, collect_time, apkNum, anaNum, risk1, risk2, risk3, risk4)
	"""
	all_apkNum = all_apkNum + int(apkNum)
	all_redNum = all_redNum + risk1
	all_orangeNum = all_orangeNum + risk2
	all_blueNum = all_blueNum + risk3
	all_failNum = all_failNum + risk4


def main():
	global all_apkNum, all_redNum, all_orangeNum, all_blueNum, all_failNum	
	site_list = { 'theappl', 'empnet', 'anruan_site1', 'anruan_site2', 'nduoa', 'pandaapp', 'hiapk', 'anzhi', 'muzhiwan'}

	#print 'SiteName \t CollectTime \t\t CollectNum \t AnalysisNum \t RED \t ORANGE \t BLUE \t Fail \t'
	for name in site_list:
		try:
			collector_statistics(name)
		except Exception as e:
			print e.message
			print "colletor '%s' data None" % name

	print '-------------------------------------------------------------------------------'
	print ' Statistics Infomation '
	print 'Collect Num \t Red Num \t Orange Num \t Blue Num \t Fail Num \t '	
	print '  %s        \t   %s    \t   %s       \t   %s     \t   %s     \t ' % \
			(all_apkNum, all_redNum, all_orangeNum, all_blueNum, all_failNum)
	

if __name__ == "__main__":
	
	try:
		main()
	except Exception as e:
		print e.message
