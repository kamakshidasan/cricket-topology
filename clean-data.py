import pandas as pd
from helper import *

x1 = -3.0
x2 = 13.0
y1 = -1.5
y2 = 1.5

df = pd.read_csv('all-ipl.csv')

cleaned_df =  df[(df['PITCHED_X'] > x1) & (df['PITCHED_X'] < x2) & (df['PITCHED_Y'] > y1) & (df['PITCHED_Y'] < y2)]
cleaned_df = cleaned_df[['INNINGS_OVER_BALL', 'BOWLER', 'BATSMAN', 'DEBIT', 'CREDIT', 'PITCHED_X', 'PITCHED_Y']]

cleaned_df.to_csv('clean-all-ipl.csv', index = False)

print df.shape
print cleaned_df.shape

#for selected_bowler in bowlers_list:
for selected_bowler in batsman_list:
	# use bowler, if you want the actual data without being cleaned
	#bowler = df[df['BOWLER'] == selected_bowler]
	#cleaned_bowler = cleaned_df[cleaned_df['BOWLER'] == selected_bowler]
	#cleaned_bowler = cleaned_bowler[['PITCHED_X', 'PITCHED_Y', 'DEBIT']]
	
	
	# use for credit for batsman
	bowler = df[df['BATSMAN'] == selected_bowler]
	cleaned_bowler = cleaned_df[cleaned_df['BATSMAN'] == selected_bowler]
	cleaned_bowler = cleaned_bowler[['PITCHED_X', 'PITCHED_Y', 'CREDIT']]

	# place additional points on the boundary
	cleaned_bowler.loc[len(cleaned_bowler)] = [x1, y1, 0]
	cleaned_bowler.loc[len(cleaned_bowler)] = [x1, y2, 0]
	cleaned_bowler.loc[len(cleaned_bowler)] = [x2, y1, 0]
	cleaned_bowler.loc[len(cleaned_bowler)] = [x2, y2, 0]
	
	cleaned_bowler = cleaned_bowler.round(3)

	# you don't nead the headers for writing to a xyz file
	#cleaned_bowler.to_csv(CLEANED_BOWLERS_DIRECTORY + selected_bowler + '.xyz', index = False, header = False)
	cleaned_bowler.to_csv(CLEANED_BATSMAN_DIRECTORY + selected_bowler + '.xyz', index = False, header = False)

	#print cleaned_bowler

	before_cleaning = bowler.shape[0]
	after_cleaning = cleaned_bowler.shape[0]
	difference_cleaning = after_cleaning - before_cleaning
	percentage_cleaning = str(int((float(difference_cleaning)/float(before_cleaning))*100)) + '%'

	print selected_bowler, before_cleaning, after_cleaning, percentage_cleaning

