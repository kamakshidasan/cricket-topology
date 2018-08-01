import matplotlib.pyplot as plt
import pandas as pd
from urllib2 import urlopen 
import numpy as np

#nba = pd.read_csv('comparing-bowlers.csv', index_col=0, delimiter = ',')

interpolation_type = 'krg'
distance_measure = 'bottleneck'
file_name = 'comparing-batsmen-'+interpolation_type+'-' + distance_measure + '.csv'

#file_name = 'comparisons/comparing-batsmen-cricmetric.csv'

nba = pd.read_csv(file_name, index_col=0, delimiter = ',')


max_value =  max(nba.max())
min_value =  min(nba.min())


nba_sort = nba


# Plot it out
fig, ax = plt.subplots()
#heatmap = ax.pcolor(nba_sort, cmap=plt.cm.YlGnBu, alpha=1.0)
heatmap = ax.pcolor(nba_sort, cmap=plt.cm.coolwarm, alpha=1.0)

fig = plt.gcf()
fig.set_size_inches(8,11)

# turn off the frame
ax.set_frame_on(False)

# put the major ticks at the middle of each cell
ax.set_yticks(np.arange(nba_sort.shape[0])+0.5, minor=False)
ax.set_xticks(np.arange(nba_sort.shape[1])+0.5, minor=False)

# want a more natural, table-like display
ax.invert_yaxis()
ax.xaxis.tick_top()



labels = [
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

labels = [
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

# note I could have used nba_sort.columns but made "labels" instead
ax.set_xticklabels(labels, minor=False) 
ax.set_yticklabels(nba_sort.index, minor=False)

# rotate the 
plt.xticks(rotation=90)

ax.grid(False)

# Turn off all the ticks
ax = plt.gca()

for t in ax.xaxis.get_major_ticks(): 
    t.tick1On = False 
    t.tick2On = False 
for t in ax.yaxis.get_major_ticks(): 
    t.tick1On = False 
    t.tick2On = False

cb = plt.colorbar(heatmap)
cb.outline.set_visible(False)
cb.set_ticks([])

plt.subplots_adjust(left=0.18, bottom=0.03, right=0.88, top=0.75, wspace=0.20, hspace=0.20)
plt.show()
