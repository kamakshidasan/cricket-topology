awk 'FNR==1 && NR!=1{next;}{print}' *.csv > all-ipl.csv
