#!/usr/bin/python3

import requests
import json
import urllib3
from datetime import date, timedelta
import argparse
import sys
import logging
import logging.handlers
import platform
import time
import operator

if sys.version_info<(3,0,0):
   sys.stderr.write("You need python 3 or later to run this script\n")
   exit(1)


parser = argparse.ArgumentParser(description='This script retrieves the list of DDoS attacks that occured the last X number of days and writes it to a file (-f), writes it to syslog (-l) or outputs it to the terminal (if -f or -l are not set).')
parser.add_argument('-k','--key', help='Specify an API key',required=True)
parser.add_argument('-u','--user',help='Specify a username', required=True)
parser.add_argument('-d','--days',help='Specify the number of days of historical info to retrieve', required=True)
parser.add_argument('-f','--file',help='Specify the path and filename of the log file to write', required=False)
parser.add_argument('-l','--limit',help='Specify the number of events to limit the results to (default is unlimited)', required=False, default=0)
parser.add_argument('-s','--syslog', help='Specify a destination to send the entries via syslog',required=False)
args = parser.parse_args()


# set the value of these strings from the command line arguments
api_key = args.key
username = args.user
days = args.days
file = args.file
limit = args.limit
syslog = args.syslog

# set date as the number of days specified in the past
date = date.today() - timedelta(int(days))

# Disable the SSL Cert warnings on a self signed cert
#urllib3.disable_warnings()

# Set up the payload
payload = {'username': username, 'api_key': api_key, 'modifiedSince': date, 'limit': limit}

try:
# Make the API get request
# Add verify=False at the end if there is a self signed cert
# updating for v2 of the API
    response = requests.get('https://dis-demo2.cablelabs.com/api/v1/data_distribution_resource/', params=payload)

except requests.exceptions.HTTPError as e:
    print (e)
    sys.exit(1)
except requests.exceptions as e:
    print (e)
    sys.exit(1)

# Put the json results into a dictionary
data = response.json()


# If var file is not set nor var syslog, then just print out the results to STDOUT 
if file is None and syslog is None:
# Iterate over all the keys
    for keys in data.keys():
# If the key is "outputData" then we want to start iterating over that dictonary b/c it has the info we want
        if keys == u'outputData':
# Get the number of key, value pairs in the dictonary and then iterate over each one
            for i in range(len(data[keys])):
# Convert the dictoary to a list of tuples.  Each tuple has the key, value from the dict.  Then sort it
                sorted_list=sorted(data[keys][i].items(), key=operator.itemgetter(0))
# Create a blank list to put all the keys (first element of each tuple)
                key_list=[]
# Iterate over all the tuples in the list
                for key in sorted_list:
# Append each key (first element of each tuple) into a list
                    key_list.append(key[0])
# Figure out if "City" is in this list
                if "City" not in key_list:
# If it isn't then add the tuple City, N/A to the list
                    sorted_list.append(("City","N/A"))
# We need to sort this list again since we just added a new tuple to it
                    sorted_list.sort()
# Figure out if "State" is in this list
                if "State" not in key_list:
# If it isn't then add the tuple State, N/A to the list
                    sorted_list.append(("State","N/A"))
# We need to sort this list again since we just added a new tuple to it
                    sorted_list.sort()
# Iterate over each tuple in the list and print them out
                for item in sorted_list:
                    print ("{}={},".format(item[0],item[1]), end=' ')
                print ('\n')

# If var file is not empty then write response to a file
if file is not None:

# Open up the log file to append data to it
    text_file = open(file, "a")
  
# Iterate over all the keys
    for keys in data.keys():
# If the key is "outputData" then we want to start iterating over that dictonary b/c it has the info we want
        if keys == u'outputData':
# Get the number of key, value pairs in the dictonary and then iterate over each one
            for i in range(len(data[keys])):
# Convert the dictoary to a list of tuples.  Each tuple has the key, value from the dict.  Then sort it
                sorted_list=sorted(data[keys][i].items(), key=operator.itemgetter(0))
# Create a blank list to put all the keys (first element of each tuple)
                key_list=[]
# Iterate over all the tuples in the list
                for key in sorted_list:
# Append each key (first element of each tuple) into a list
                    key_list.append(key[0])
# Figure out if "City" is in this list
                if "City" not in key_list:
# If it isn't then add the tuple City, N/A to the list
                    sorted_list.append(("City","N/A"))
# We need to sort this list again since we just added a new tuple to it
                    sorted_list.sort()
# Figure out if "State" is in this list
                if "State" not in key_list:
# If it isn't then add the tuple State, N/A to the list
                    sorted_list.append(("State","N/A"))
# We need to sort this list again since we just added a new tuple to it
                    sorted_list.sort()
# Iterate over each tuple in the list and write them to a file:
                for item in sorted_list:
                    text_file.write("{}={},".format(item[0],item[1]))
                text_file.write('\n')
# Sleep for 2/10th of a second so that the syslog server will see each new line as a new log entry
                time.sleep(.2)

# Close the log file
    text_file.close()


# If syslog var is not empty then send responses out via syslog
if syslog is not None:

# Create the logger
    my_logger = logging.getLogger('MyLogger')

# We will pass the message as INFO
    my_logger.setLevel(logging.INFO)

# Define SyslogHandler
# 514 = Syslog port , You need to specify the port which you have defined ,by default it is 514 for Syslog)
    handler = logging.handlers.SysLogHandler(address = (syslog,514))

# Apply handler to my_logger
    my_logger.addHandler(handler)

# Iterate over all the keys
    for keys in data.keys():
# If the key is "outputData" then we want to start iterating over that dictonary b/c it has the info we want
        if keys == u'outputData':
# Get the number of key, value pairs in the dictonary and then iterate over each one
            for i in range(len(data[keys])):
# Create a blank string 
                syslog_message=""
# Convert the dictoary to a list of tuples.  Each tuple has the key, value from the dict.  Then sort it
                sorted_list=sorted(data[keys][i].items(), key=operator.itemgetter(0))
# Create a blank list to put all the keys (first element of each tuple)
                key_list=[]
# Iterate over all the tuples in the list
                for key in sorted_list:
# Append each key (first element of each tuple) into a list
                    key_list.append(key[0])
# Figure out if "City" is in this list
                if "City" not in key_list:
# If it isn't then add the tuple City, N/A to the list
                    sorted_list.append(("City","N/A"))
# We need to sort this list again since we just added a new tuple to it
                    sorted_list.sort()
# Figure out if "State" is in this list
                if "State" not in key_list:
# If it isn't then add the tuple State, N/A to the list
                    sorted_list.append(("State","N/A"))
# We need to sort this list again since we just added a new tuple to it
                    sorted_list.sort()
# Iterate over each tuple in the list and write them to a file:
                for item in sorted_list:
                    syslog_message=syslog_message+str(item[0])+"="+str(item[1])+","
                my_logger.info(syslog_message)
