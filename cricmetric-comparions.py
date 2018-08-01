import csv
from scipy.stats import pearsonr
from numpy import median

cricmetric = {}

interpolation_method = 'idw'
distance_method = 'bottleneck'

interpolation_methods = ['idw', 'nn', 'spline', 'krg']
distance_methods = ['earthmovers', 'w1', 'bottleneck']

with open("comparisons/comparing-batsmen-cricmetric.csv", "r") as f:
	reader = csv.reader(f, delimiter="\t")
	headers = next(reader, None)
	
	for i, line in enumerate(reader):
		line = line[0].split(',')
		player = line[0]
		line.remove(player)
		line = list(map(int, line))
		cricmetric[player] = line


for interpolation_method in interpolation_methods:
	for distance_method in distance_methods:

		dictionary = {}
		ranking = []


		file_name = 'comparisons/comparing-batsmen-' + interpolation_method + '-' + distance_method + '.csv'
		with open(file_name, "r") as f:
			reader = csv.reader(f, delimiter="\t")
			headers = next(reader, None)
			
			for i, line in enumerate(reader):
				line = line[0].split(',')
				player = line[0]
				line.remove(player)
				line = list(map(int, line))
				dictionary[player] = line


		for player in cricmetric.keys():
			pvalue = pearsonr(cricmetric[player], dictionary[player])[0]
			ranking.append(pvalue)
			#print player, pvalue

		average_value = round(sum(ranking)/len(ranking), 3)
		median_value = round(median(ranking),3)

		print interpolation_method, distance_method, average_value, median_value
