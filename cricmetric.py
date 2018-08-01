import csv

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

reader = csv.reader(open('cricmetric.csv', 'r'))
headers = next(reader, None)

d = {}
differences = {}
maximum_score = {}

for row in reader:
	k, v = row
	d[k] = float(v)

for bowler1 in d.keys():
	a = d[bowler1]
	differences[bowler1] = {}
	maximum_score[bowler1] = 0.0
	
	for bowler2 in d.keys():
	
		if ((bowler1 in players) and (bowler2 in players)):
			b = d[bowler2]
			c = round(abs(b-a),3)
			
			differences[bowler1][bowler2] = c
			maximum_score[bowler1] = max(maximum_score[bowler1], c)
			
			#print bowler1 + "," + bowler2 + "," + str(c)


for bowler1 in players:
	for bowler2 in players:
		differences[bowler1][bowler2] /= maximum_score[bowler1]


tree_file = open('comparing-batsmen-cricmetric.csv', 'w')
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
