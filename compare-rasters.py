import numpy as np
from matplotlib import pyplot as plt 
import os
import time
from pyemd import emd_samples


folder_path = 'rasters-bowlers/'

d = {}
differences = {}
maximum_score = {}

players = [
'stevesmith',
'brendonmccullum',
'sureshraina',
'dineshkarthik',
'shikhardhawan',
'manishpandey',
'msdhoni',
'aaronfinch',
'shanewatson',
'viratkohli',
'robinuthappa',
'chrisgayle',
'davidwarner',
'rohitsharma',
'abdevilliers'
]

players = [
'bhuvneshwarkumar',
'mornemorkel',
'umeshyadav',
'lasithmalinga',
'rajatbhatia',
'chrismorris',
'harbhajansingh',
'dalesteyn',
'sunilnarine',
'dwaynebravo',
'ravichandranashwin',
'mitchelljohnson'
]

bowler_names = os.listdir(folder_path)
bowler_list = []

for bowler_name in bowler_names:

	#batsman = folder_path + os.path.sep +  bowler_name
	batsman = folder_path + bowler_name
	
	bowler = (bowler_name.split('.')[0]).replace(" ", "")
	
	a  = np.loadtxt(batsman, skiprows=6).flatten()
	a /= np.max(np.abs(a),axis=0)
	a *= (39.0/a.max())
	a = a.astype(int)
	
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
			c = emd_samples(a, b, bins=40)
			
			differences[bowler1][bowler2] = c
			
			maximum_score[bowler1] = max(maximum_score[bowler1], c)
			
			#print bowler1 + "," + bowler2 + "," + str(c)


for bowler1 in players:
	for bowler2 in players:
		differences[bowler1][bowler2] /= maximum_score[bowler1]



print 'bowler', 
for bowler in players:
	print bowler, 
print ''
	
for bowler1 in players:
	print bowler1, 
	for bowler2 in players:
		print round(differences[bowler1][bowler2],3), 
	print ''
