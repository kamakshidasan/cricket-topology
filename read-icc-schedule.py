import urllib, json, csv
from urlparse import urljoin
from helper import *
import dateutil.parser
import pandas as pd

games_path = 'icc-schedules.json'

unique_matches = {}

with open(games_path) as games_file:
	data = json.load(games_file)
	page_size = len(data[CONTENT])
		
	for index in range(0, page_size):
		match = data[CONTENT][index]

		match_id = match[SCHEDULE_ENTRY][MATCH_IDENTIFIER][IDENTIFIER]
		tournament_name = match[TOURNAMENT_IDENTIFIER][NAME]
		match_name = match[SCHEDULE_ENTRY][MATCH_IDENTIFIER][NAME]
		match_type = match[SCHEDULE_ENTRY][MATCH_TYPE]
	
		match_datetime = dateutil.parser.parse(match['timestamp'])

		team1 = match[SCHEDULE_ENTRY]['team1']
		team2 = match[SCHEDULE_ENTRY]['team2']
		
		print match_id
		
		hawkeye_link = get_data_url([ICC_API_URL, FIXTURES, str(match_id), DATABASE, TRAJECTORY])
		

		try:
			#match_outcome = match[SCHEDULE_ENTRY]['matchStatus']['text']
			innings_count = len(team1['innings']) + len(team2['innings'])
		except:
			#match_outcome = None
			try:
				innings_count = len(team1['innings'])
			except:
				innings_count = 0
	
		home_team = team1['team']['fullName']
		away_team = team2['team']['fullName']
		
		match_date = match_datetime.strftime("%Y-%m-%d")
		match_time = match_datetime.strftime("%H:%M")
	
		match_data = [match_id, match_date, match_time, home_team, away_team, match_name, tournament_name, match_type, innings_count, hawkeye_link]
		unique_matches[match_id] = match_data
		
		print match_data

with open('icc-schedule.csv', 'wb') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerow(["icc_match_id", "match_date", "match_time", "home_team", "away_team", "match_name", "tournament_name", "match_type", "innings_count", "hawkeye_link"])
	for match in unique_matches.keys():
		writer.writerow(unique_matches[match])
		
# sort on the basis of date and write back to file
df = pd.read_csv('icc-schedule.csv')
df = df.sort_values('match_date')
df.to_csv('icc-schedule.csv', index=False)
