from pyemd import emd
import numpy as np
from scipy.spatial import distance

d = np.load('all-batsmen-histograms.npy').item()

#print 'bowler1,bowler2,difference'

differences = {}

for bowler1 in d.keys():
	a = d[bowler1]
	differences[bowler1] = {}
	
	for bowler2 in d.keys():
		b = d[bowler2]
		
		a = a.astype('float')
		b = b.astype('float')
		c = distance.cdist((np.array([a])).T, (np.array([b])).T, 'euclidean')
		difference = round(emd(a, b, c),2)
		
		differences[bowler1][bowler2] = difference
		
		#print bowler1 + "," + bowler2 + "," + str(difference)

print 'bowler', 
for bowler in d.keys():
	print bowler, 
print ''
	
for bowler1 in d.keys():
	print bowler1, 
	for bowler2 in d.keys():
		print differences[bowler1][bowler2], 
	print ''
