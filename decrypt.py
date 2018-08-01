# This is the most sloppiest code I have ever written

import json, csv, collections, copy, pprint
import execjs
import numpy as np

def flatten(d, parent_key='', sep='_'):
	items = []
	for k, v in d.items():
		new_key = parent_key + sep + k if parent_key else k
		if isinstance(v, collections.MutableMapping):
			items.extend(flatten(v, new_key, sep=sep).items())
		else:
			items.append((new_key, v))
	return dict(items)

def compile_pulse():
	with open('pulse.js', 'r') as myfile:
		pulse_script = myfile.read()
	pulse = execjs.compile(pulse_script)
	return pulse

def read_matches(filename):
	with open(filename) as f:
		matches = f.readlines()
	matches = [x.strip() for x in matches]
	return matches

def get_stats(match_name):
	match_name = match_name.split("-")
	match_name.insert(1, "stats")
	
	stats_file = '-'.join(match_name)
	return data_directory + stats_file + '.json'

def get_stats_data(stats_file):
	with open(stats_file) as data_file:
		stats = json.load(data_file)
	return stats["data"]	

def read_stats(stats_file):
	try:
		with open(stats_file) as data_file:
			stats = json.load(data_file)

		statistics_data = {}
		for statistics in stats["data"]:
			for ball in statistics.keys():
				statistics_data[ball] = statistics[ball].split(",")[:-3]
				#print ball, statistics_data[ball]
		return statistics_data

	except:
		print 'Read Stats Fatal Error Happened'
		return False

def get_traj(match_name):
	match_name = match_name.split("-")
	match_name.insert(1, "traj")
	
	traj_file = '-'.join(match_name)
	return data_directory + traj_file + '.json'

def read_traj(statistics_data, traj_file):
	try:
		with open(traj_file) as data_file:	
			traj = json.load(data_file)

		for index in range(0, len(traj["data"])):
			ball, statistic = traj["data"][index].items()[0]
			print ball
			
		return statistics_data
	except:
		pass

# We again use the initial order from the data itself
def write_csv(match_name, appended_data, stats_data, players_data):
	with open('parsed/' + match_name + '.csv', 'wb') as test_file:

		file_writer = csv.writer(test_file)
		file_writer.writerow(headers)

		for index in range(0, len(stats_data)):
			ball, statistic = stats_data[index].items()[0]
			complete_data = appended_data[ball]

			# Make ball 0-indexed
			ball = ball.split('.')
			ball[1] = str(int(ball[1]) - 1)
			ball = '.'.join(ball)
			
			# add year and match information
			# IPLT20-ipl2012-01
			match_info = (match_name.split('IPLT20-ipl'))[1]
			[match_year, match_index] = match_info.split('-')
			match_index = str(int(match_index))
			ball = match_year + '.' + match_index + '.' + ball
			

			complete_data.insert(0, ball)
			complete_data[2] = players_data[int(complete_data[2])]
			complete_data[3] = players_data[int(complete_data[3])]
			complete_data[4] = players_data[int(complete_data[4])]

			if complete_data[6] != '-1':
				complete_data[6] = players_data[int(complete_data[6])]
			
			# just deleting stuff
			# this is an extremely bad way of doing it
			del complete_data[-8]
			del complete_data[-11+1]
			del complete_data[-12+2]
			del complete_data[-13+3]
			del complete_data[-16+4]
			del complete_data[-18+5]
			complete_data.insert(0, match_year)
			
			file_writer.writerow(complete_data)


def write_error(match_name):
	with open('errors.csv', 'wb') as test_file:
		file_writer = csv.writer(test_file)
		file_writer.writerow(match_name)


def get_players(match_name):
	match_name = match_name.split("-")
	match_name.insert(1, "players")
	
	players_file = '-'.join(match_name)
	return data_directory + players_file + '.json'

def read_players(players_file):
	try:
		with open(players_file) as data_file:
			players = json.load(data_file)

		players_data = {}
		for player in players["teams"][0]["players"]:
			players_data[player["id"]] = player["fullName"]

		for player in players["teams"][1]["players"]:
			players_data[player["id"]] = player["fullName"]

		return players_data
	except:
		print 'Read Players Fatal Error Happened'
		return False

if __name__ == "__main__":
	pulse = compile_pulse()

	data_directory = "data/"
	matches = read_matches("match_list.txt")
			
	global_headers = ["YEAR", "INNINGS_OVER_BALL","BATSMAN","BOWLER",
			"BOWL_SPEED","CREDIT","DEBIT","IS_RHB",\
			"PITCHED_X","PITCHED_Y","STUMPS_Y","STUMPS_Z","LANDING_X","LANDING_Y"]

	for match in matches:
		#match = 'ODI-champtrophy-2013-12'
		headers = copy.deepcopy(global_headers)

		stats_file = get_stats(match)
		statistics = read_stats(stats_file)

		if statistics == False:
			write_error(match)

		appended_statistics = read_traj(statistics, get_traj(match))
		players_data = read_players(get_players(match))

		if players_data == False:
			write_error(match)
	
		write_csv(match, appended_statistics, get_stats_data(stats_file), players_data)
		print match
