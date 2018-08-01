import urllib, json
from urlparse import urljoin
from helper import *

teams = {}

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

print matches_url

response = urllib.urlopen(matches_url)
data = json.loads(response.read())
number_pages = data[PAGE_INFORMATION][PAGE_NUMBER]

for page in range(0, number_pages):
	search_parameters[PAGE] = page
	page_url = fixtures_url + '?' + urllib.urlencode(search_parameters)
	
	try:
		response = urllib.urlopen(page_url)
		data = json.loads(response.read())

		page_size = len(data[CONTENT])
		
		save_data(page_url, 'schedule', ['schedule', str(page)], JSON_EXTENSION)
		
		print page+1, '/', number_pages
		
		
		for index in range(0, page_size):
			match = data[CONTENT][index]
			
			team1 = match[SCHEDULE_ENTRY]['team1']
			team2 = match[SCHEDULE_ENTRY]['team2']

			teams[team1['team']['fullName']] = team1['team']['id']
			teams[team2['team']['fullName']] = team2['team']['id']
	
	except Exception, e:
		print 'Page Number: ', page, 'idiots', e
		
for team in teams.keys():
	print team, teams[team]

file_names = []
contents = []
file_content = {}

# List all files in data directory ending
for file in os.listdir(DATA_DIRECTORY):
	if file.endswith(JSON_EXTENSION):
		file_names.append(file)
		
file_names = sorted(file_names, key=lambda item: (int(item.partition('-')[0])
						if item[1].isdigit() else float('inf'), item))

# Iterate through these files and add them to memory
for file_name in file_names:
	file_path = os.path.join(DATA_DIRECTORY, file_name)
	
	with open(file_path) as response:
		data = json.loads(response.read())
		
		#print len(data['content'])
		contents.extend(data['content'])

file_content['content'] = contents

json.dump(file_content, open('icc-schedules.json', 'wb'))
