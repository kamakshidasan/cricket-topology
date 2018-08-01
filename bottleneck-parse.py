import csv

interpolation_method = 'krg'

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

differences = {}
maximum_score = {}

for player in players:
	differences[player] = {}
	maximum_score[player] = 0.0
	
reader = csv.reader(open('bottleneck-values/comparing-batsmen-'+interpolation_method+'-bottleneck.csv', 'r'))


for row in reader:
	player1, player2, value = row
	try:
		differences[player1][player2] = float(value)
		maximum_score[player1] = max(maximum_score[player1], differences[player1][player2])
	except:
		continue


for bowler1 in players:
	for bowler2 in players:
		differences[bowler1][bowler2] /= maximum_score[bowler1]


tree_file = open('comparing-batsmen-'+interpolation_method+'-bottleneck.csv', 'w')
writer = csv.writer(tree_file, delimiter=',')

player_names = []
player_names.append('bowler')
for bowler in players:
	player_names.append(bowler)

writer.writerow(player_names)


for bowler1 in players:
	player_comparison = []
	for bowler2 in players:
		comparison_value = round(differences[bowler1][bowler2],3)
		player_comparison.append(comparison_value)
	
	
	seq = sorted(player_comparison)
	player_ranking = [seq.index(v) for v in player_comparison]
	
	player_ranking.insert(0, bowler1)
	writer.writerow(player_ranking)

tree_file.close()
