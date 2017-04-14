#!/usr/bin/python

import requests
import json
import urllib3
from datetime import date, timedelta
import argparse
import sys
import logging
import logging.handlers
import platform

# If we are running a version of python less than 2.7, then exit and throw up an error.
if sys.version_info<(2,7,0):
   sys.stderr.write("You need python 2.7+ or later to run this script\n")
   exit(1)

parser = argparse.ArgumentParser(description='This script retrieves the list of DDoS attacks that occured the last X number of days and writes it to a file (-f), writes it to syslog (-l) or outputs it to the terminal (if -f or -l are not set).')
parser.add_argument('-k','--key', help='Specify an API key',required=True)
parser.add_argument('-u','--user',help='Specify a username', required=True)
parser.add_argument('-d','--days',help='Specify the number of days of historical info to retrieve', required=True)
parser.add_argument('-f','--file',help='Specify the path and filename of the log file to write', required=False)
parser.add_argument('-l','--syslog', help='Specify a destination to send the entries via syslog',required=False)
args = parser.parse_args()


# set the value of these strings from the command line arguments
api_key = args.key
username = args.user
days = args.days
file = args.file
syslog = args.syslog

# set date as the number of days specified in the past
date = date.today() - timedelta(int(days))

# Disable the SSL Cert warnings on a self signed cert (maybe remove this and the verify=False if they get a valid SSL cert!)
urllib3.disable_warnings()

# Set up the payload
payload = {'username': username, 'api_key': api_key, 'modifiedSince': date,}

# Make the API get request
# Add verify=False at the end if there is a self signed cert
response = requests.get('https://dis-demo.cablelabs.com/api/v1/data_distribution_resource/', params=payload)

# Put the json results into a dictionary
data = response.json()

# If var file is not set nor var syslog, then just print out the results 
if file is None and syslog is None:
        for i in data['dis-data']:
                print ("IP_Address=%s Number_of_Times_Seen=%s Attack_Types=\"%s\" City=\"%s\" State=%s Country=%s First_Time_Seen=%s Last_Time_Seen=%s Total_BPS=%s Total_PPS=%s \n " % (i['IPaddress'], i['numberOfTimesSeen'], i['attackTypes'], i['City'], i['State'], i['Country'], i['firstTimeSeen'], i['lastTimeSeen'], i['totalBPS'], i['totalPPS']))



# If var file is not empty then write response to a file
if file is not None:

# Open up the log file
#        text_file = open(file, "w")
        text_file = open(file, "a")
  
#For each entry, write a line in the log file
        for i in data['dis-data']:
                text_file.write("DDoS_InfoSec_Sharing IP_Address=%s Number_of_Times_Seen=%s Attack_Types=\"%s\" City=\"%s\" State=%s Country=%s First_Time_Seen=%s Last_Time_Seen=%s Total_BPS=%s Total_PPS=%s \n " % (i['IPaddress'], i['numberOfTimesSeen'], i['attackTypes'], i['City'], i['State'], i['Country'], i['firstTimeSeen'], i['lastTimeSeen'], i['totalBPS'], i['totalPPS']))

# Close the log file
        text_file.close()

# If syslog var is not empty then send responses out via syslog
if syslog is not None:

#Create you logger. Please note that this logger is different from  ArcSight logger.
        my_logger = logging.getLogger('MyLogger')

#We will pass the message as INFO
        my_logger.setLevel(logging.INFO)

#Define SyslogHandler
#X.X.X.X =IP Address of the Syslog Collector(Connector Appliance,Loggers  etc.)
#514 = Syslog port , You need to specify the port which you have defined ,by default it is 514 for Syslog)
        handler = logging.handlers.SysLogHandler(address = (syslog,514))

#apply handler to my_logger
        my_logger.addHandler(handler)

# For each entry, send a syslog message
        for i in data['dis-data']:
                my_logger.info("%s DDoS_InfoSec_Sharing IP_Address=%s Number_of_Times_Seen=%s Attack_Types=\"%s\" City=\"%s\" State=%s Country=%s First_Time_Seen=%s Last_Time_Seen=%s Total_BPS=%s Total_PPS=%s \n " % ( platform.node(), i['IPaddress'], i['numberOfTimesSeen'], i['attackTypes'], i['City'], i['State'], i['Country'], i['firstTimeSeen'], i['lastTimeSeen'], i['totalBPS'], i['totalPPS']))
