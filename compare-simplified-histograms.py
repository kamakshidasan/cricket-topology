import numpy as np
from matplotlib import pyplot as plt 
import os
import time
from pyemd import emd_samples
import csv


#folder_path = 'terrain-bowlers/'

interpolation_type = 'idw'
folder_path = 'terrain-batsmen-'+interpolation_type+'/'

d = {}
differences = {}
maximum_score = {}

players = [
'Bhuvneshwar Kumar',
'Morne Morkel',
'Umesh Yadav',
'Lasith Malinga',
'Rajat Bhatia',
'Chris Morris',
'Harbhajan Singh',
'Dale Steyn',
'Sunil Narine',
'Dwayne Bravo',
'Ravichandran Ashwin',
'Mitchell Johnson'
]

players = [
'Steve Smith',
'Brendon McCullum',
'Suresh Raina',
'Dinesh Karthik',
'Shikhar Dhawan',
'Manish Pandey',
'MS Dhoni',
'Aaron Finch',
'Shane Watson',
'Virat Kohli',
'Robin Uthappa',
'Chris Gayle',
'David Warner',
'Rohit Sharma',
'de Villiers'
]

players = [
'Amit Mishra',
'Dwayne Bravo',
'Axar Patel',
'James Faulkner',
'Praveen Kumar',
'Chris Morris',
'Shahbaz Nadeem',
'Mitchell McClenaghan',
'Mohit Sharma',
'Mitchell Johnson',
'Morne Morkel',
'Dhawal Kulkarni',
'Rajat Bhatia',
'Harbhajan Singh',
'Ashok Dinda',
'Shane Watson',
'Ravichandran Ashwin',
'Sandeep Sharma',
'Jasprit Bumrah',
'Piyush Chawla',
'Ashish Nehra',
'Yuzvendra Chahal',
'Bhuvneshwar Kumar',
'Dale Steyn',
'Sunil Narine',
'Umesh Yadav',
'Vinay Kumar',
'Zaheer Khan',
'Ravindra Jadeja'
]

players = [
'Gautam Gambhir',
'Suresh Raina',
'Steve Smith',
'Virat Kohli',
'MS Dhoni',
'Robin Uthappa',
'Shikhar Dhawan',
'Shane Watson',
'de Villiers',
'Michael Hussey',
'Rohit Sharma',
'David Warner',
'Manish Pandey',
'Yusuf Pathan',
'Dinesh Karthik',
'Parthiv Patel',
'Aaron Finch',
'Dwayne Smith',
'Murali Vijay',
'Sanju Samson',
'Ajinkya Rahane',
'David Miller',
'Yuvraj Singh',
'Brendon McCullum',
'Chris Gayle',
'Kieron Pollard',
]

bowler_names = os.listdir(folder_path)
bowler_list = []

for bowler_name in bowler_names:

	#batsman = folder_path + os.path.sep +  bowler_name
	batsman = folder_path + bowler_name
	
	bowler = (bowler_name.split('.'))[0]
	
	values = []
	with open(batsman, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ')
		for r in spamreader:
			row = r[0].split(',')
			value = int(row[2])
			values.append(value)
	
	a = np.asarray(values)
	
	d[bowler] = a

for bowler1 in d.keys():
	a = d[bowler1]
	differences[bowler1] = {}
	maximum_score[bowler1] = 0.0
	bowler_list.append(bowler1)
	
	for bowler2 in d.keys():
	
		if ((bowler1 in players) and (bowler2 in players)):
			b = d[bowler2]
			
			a = a.astype('float')
			b = b.astype('float')
			c = emd_samples(a, b, bins=255)
			
			differences[bowler1][bowler2] = c
			
			maximum_score[bowler1] = max(maximum_score[bowler1], c)
			
			#print bowler1 + "," + bowler2 + "," + str(c)


for bowler1 in players:
	for bowler2 in players:
		differences[bowler1][bowler2] /= maximum_score[bowler1]


#tree_file = open('comparing-bowlers.csv', 'w')
tree_file = open('comparing-batsmen-'+interpolation_type+'.csv', 'w')
writer = csv.writer(tree_file, delimiter=',')

player_names = []
player_names.append('bowler')
for bowler in players:
	player_names.append(bowler)

writer.writerow(player_names)


for bowler1 in players:
	player_comparison = []
	#player_comparison.append(bowler1)
	for bowler2 in players:
		comparison_value = round(differences[bowler1][bowler2],3)
		player_comparison.append(comparison_value)
	
	
	seq = sorted(player_comparison)
	player_ranking = [seq.index(v) for v in player_comparison]
	
	player_ranking.insert(0, bowler1)
	writer.writerow(player_ranking)

tree_file.close()
