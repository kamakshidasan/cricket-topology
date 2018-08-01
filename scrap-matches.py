import urllib, json
from urlparse import urljoin
from helper import *

fixtures_url = get_data_url([ICC_API_URL, FIXTURES])
search_parameters = {
						MATCH_TYPES: 'IPLT20',
						STARTING_DATE: '2012-01-01',
						ENDING_DATE: '2018-01-01',
						PAGE: 0
					}

# This match spoils the entire API: http://www.espncricinfo.com/series/8650/scorecard/631137
#search_parameters = {'tournamentTypes':'I',  'matchTypes':'TEST,ODI,T20I', 'startDate':'2013-06-27', 'endDate':'2013-07-09', 'page':0, 'pageSize':1}

# There seems to be no nice way to circumvent this repetition outside the loop
# You require the number of pages to be known before hand
matches_url = fixtures_url + '?' + urllib.urlencode(search_parameters)
response = urllib.urlopen(matches_url)
data = json.loads(response.read())
number_pages = data[PAGE_INFORMATION][PAGE_NUMBER]

for page in range(0, number_pages):
	search_parameters[PAGE] = page
	page_url = fixtures_url + '?' + urllib.urlencode(search_parameters)

	#print page_url
	try:
		response = urllib.urlopen(page_url)
		data = json.loads(response.read())

		page_size = len(data[CONTENT])

		for index in range(0, page_size):
			match = data[CONTENT][index]

			match_id = match[SCHEDULE_ENTRY][MATCH_IDENTIFIER][IDENTIFIER]
			tournament_name = match[TOURNAMENT_IDENTIFIER][NAME]
			match_name = match[SCHEDULE_ENTRY][MATCH_IDENTIFIER][NAME]
			match_type = match[SCHEDULE_ENTRY][MATCH_TYPE]

			match_url = get_data_url([fixtures_url, match_id])
			players_url = get_data_url([match_url, DATABASE])
			stats_url = get_data_url([match_url, DATABASE, STATISTICS])
			traj_url = get_data_url([match_url, DATABASE, TRAJECTORY])

			print match_name, match_type

			save_data(match_url, METADATA, [match_type, METADATA, match_name], JSON_EXTENSION)
			save_data(players_url, PLAYERS, [match_type, PLAYERS, match_name], JSON_EXTENSION)
			save_data(stats_url, STATISTICS, [match_type, STATISTICS, match_name], JSON_EXTENSION)
			save_data(traj_url, TRAJECTORY, [match_type, TRAJECTORY, match_name], JSON_EXTENSION)


			with open("match_list.txt", "a") as match_list:
				match_list.write(match_type + '-' + match_name + '\n')	

			#print match_url
			#print players_url
			#print stats_url
			#print traj_url
			#print ''
		
		#print 'Page Number: ', page, 'OK'
		#print json.dumps(data['content'][55], indent=4, sort_keys=True)

	except Exception, e:
		print 'Page Number: ', page, 'idiots', e
