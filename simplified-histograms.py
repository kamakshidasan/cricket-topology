import numpy as np
from matplotlib import pyplot as plt 
import os
import time
import csv

from astropy.modeling import models, fitting


all_lengths = []

#folder_path = r"C:\\Users\\lenovo\\Desktop\\rasters-bowlers"
#desktop_path = r"C:\\Users\\lenovo\\Desktop"


#folder_path = 'terrain-bowlers/'
folder_path = 'terrain-bowlers/'

histogram_dictionary = {}

bowler_names = os.listdir(folder_path)

for bowler_name in bowler_names:

	#batsman = folder_path + os.path.sep +  bowler_name
	batsman = folder_path + bowler_name
	
	bowler = (bowler_name.split('.')[0])
	
	values = []
	print batsman
	with open(batsman, 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ')
		for r in spamreader:
			row = r[0].split(',')
			value = int(row[2])
			values.append(value)
	
	a = np.asarray(values)
	
	#a  = np.loadtxt(batsman, skiprows=6).flatten()
	#a /= np.max(np.abs(a),axis=0)
	#a *= (39.0/a.max())
	#a = a.astype(int)
	
	current_histogram =  np.histogram(a,  bins = range(255))
	
	bin_heights, bin_borders = np.histogram(a, bins = range(255))
	bin_widths = np.diff(bin_borders)
	bin_centers = bin_borders[:-1] + bin_widths / 2

	t_init = models.Lorentz1D()
	fit_t = fitting.LevMarLSQFitter()
	t = fit_t(t_init, bin_centers, bin_heights)

	x_interval_for_fit = np.linspace(bin_borders[0], bin_borders[-1], 20000)
	plt.figure()
	plt.bar(bin_centers, bin_heights, width=bin_widths, label='histogram')
	plt.plot(x_interval_for_fit, t(x_interval_for_fit), label='fit', c='red', linestyle='--')
	plt.xlabel('Pixel Value')
	plt.ylabel('Count')
	plt.legend()
	
	plt.title(bowler) 
	
	#output_folder =  os.path.join(desktop_path, "histograms-bowlers", bowler + '.png')
	output_folder =  os.path.join("histograms-bowlers", bowler + '.png')
	
	
	plt.savefig(output_folder)
	plt.gcf().clear()
	
	print output_folder
	
	print current_histogram[0]
	
	all_lengths.append(len(current_histogram[1]))
	
	
	histogram_dictionary[bowler] = current_histogram[0]

print sum(all_lengths)/len(all_lengths)

np.save('all-bowlers-histograms.npy', histogram_dictionary)

#bowlers_dictionary = np.load('all-bowlers-histograms.npy').item()
