import os, re, shutil, pickle, inspect, csv, sys, math
import urllib, json
from urlparse import urljoin

############################
## Identifiers for scrapping cricket
############################

# List of constants
CSV_EXTENSION = '.csv'
PYTHON_COMMAND = 'python'
PAGE = 'page'
IDENTIFIER = 'id'
CONTENT = 'content'
NAME = 'name'
PAGE_INFORMATION = 'pageInfo'
PAGE_NUMBER = 'numPages'
SCHEDULE_ENTRY = 'scheduleEntry'
TOURNAMENT_IDENTIFIER = 'tournamentId'
MATCH_TYPE = 'matchType'
MATCH_IDENTIFIER = 'matchId'
DATABASE = 'uds'
STATISTICS = 'stats'
TRAJECTORY = 'traj'
METADATA = 'meta'
PLAYERS = 'players'
FIXTURES = 'fixtures'
COMMENTARY = 'commentary'
META = 'meta'
META_COMMENTARY = 'meta-commentary'
CUSTOMER = 'customer'
ICC = 'icc'
FEEDS = 'feeds'
CUSTOMER_INFORMATION = {CUSTOMER: ICC}
DATA_DIRECTORY = 'data/'
CLEANED_BOWLERS_DIRECTORY = 'cleaned-bowlers/'
CLEANED_BATSMAN_DIRECTORY = 'cleaned-batsman/'

TOURNAMENT_TYPES = 'tournamentTypes'
MATCH_TYPES = 'matchTypes'
STARTING_DATE = 'startDate'
ENDING_DATE = 'endDate'

TEST_MATCH = 'TEST'
ODI_MATCH = 'ODI'
TWENTY_INTERNATIONAL_MATCH = 'T20I'
INTERNATIONAL_TOURNAMENT = 'I'

JSON_EXTENSION = '.json'

ICC_API_URL = 'http://cricketapi-icc.pulselive.com'

bowlers_list = [
'Harbhajan Singh',
'Bhuvneshwar Kumar',
'Sunil Narine',
'Umesh Yadav',
'Amit Mishra',
'Lasith Malinga',
'Ravichandran Ashwin',
'Mohit Sharma',
'Ravindra Jadeja',
'Piyush Chawla',
'Praveen Kumar',
'Dwayne Bravo',
'Morne Morkel',
'Ashish Nehra',
'Axar Patel',
'James Faulkner',
'Sandeep Sharma',
'Vinay Kumar',
'Shane Watson',
'Yuzvendra Chahal',
'Zaheer Khan',
'Dale Steyn',
'Mitchell Johnson',
'Rajat Bhatia',
'Jasprit Bumrah',
'Karn Sharma',
'Chris Morris',
'Shahbaz Nadeem',
'Mitchell McClenaghan',
'Dhawal Kulkarni',
'Ashok Dinda'
]

batsman_list = [
'AB de Villiers',
'David Warner',
'Chris Gayle',
'Kieron Pollard',
'David Miller',
'Suresh Raina',
'Yusuf Pathan',
'Dwayne Smith',
'MS Dhoni',
'Shane Watson',
'Virat Kohli',
'Rohit Sharma',
'Robin Uthappa',
'Steve Smith',
'Aaron Finch',
'Brendon McCullum',
'Yuvraj Singh',
'Faf du Plessis',
'Ambati Rayudu',
'Shaun Marsh',
'Dinesh Karthik',
'Sanju Samson',
'Gautam Gambhir',
'Shikhar Dhawan',
'Parthiv Patel',
'Manish Pandey',
'Ajinkya Rahane',
'Michael Hussey',
'Murali Vijay'
]

def save_data(data_url, folder_name, file_arguments, file_extension):
	file_name = join_strings(file_arguments) + file_extension
	#urllib.urlretrieve(data_url, folder_name + '/' + file_name)
	#return folder_name + '/' + file_name

	urllib.urlretrieve(data_url, 'data/' + file_name)
	return 'data/' + file_name

def get_data_url(arguments):
	return '/'.join(str(argument) for argument in arguments)

# get working directory and add '/' at the end
def cwd():
	return os.path.join(os.getcwd(), '')

# get path of current file
def current_path():
	return os.path.abspath(inspect.getfile(inspect.currentframe()))
	
# join two strings
def join_strings(strings):
	return '-'.join(strings)
