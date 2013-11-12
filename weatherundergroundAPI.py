#!/usr/bin/python
'''
########################################################################################

Retrieve Historical Weather Data using the Weatherunderground API

Read more at http://www.wunderground.com/weather/api/d/docs?d=resources/code-samples#T43sEjcDrJbDoyIo.99

__author__ = "Drew Smith" 
__email__ = "ajsmith007@gmail.com"
__version__ = "1.0.0"
__status__ = "Demonstration"
__copyright__ = Copyright 2013, Drew Smith"

Created on: October 1, 2013

########################################################################################
'''

import urllib2 
import json
import time

# ## Current Data
# current_conditions ='http://api.wunderground.com/api/34e4d065c41d49d4/geolookup/conditions/q/CA/San_Francisco.json' 
# 
# f = urllib2.urlopen(current_conditions) 
# json_string = f.read() 
# parsed_json = json.loads(json_string)
# #print parsed_json
# location = parsed_json['location']['city'] 
# temp_f = parsed_json['current_observation']['temp_f'] 
# print "Current temperature in %s is: %s" % (location, temp_f) 
# f.close()

## Yelp Dataset Challenge - Phoenix AZ
# Start Date:    "2005-03-07 MST"
# End Date:      "2013-01-05 MST"

## GET Historical Data
prefix_key = 'http://api.wunderground.com/api/<InsertYourAPIKeyHere>/history_'
startdate = 20050701 
numdays = 31
max_calls = 10 # weatherunderground API limit per minute
query = '/q/'
state = 'AZ'
slash = '/'
city = 'Phoenix'
dot_json = '.json'

## Open file for writing
weatherCityState = 'weather' + city + state
foutput = open(weatherCityState + str(startdate) + '.csv','w')

calls = 0
for d in range(0, numdays):
    date = str(startdate + d)
    
    historical = prefix_key + date  + query + state + slash  + city + dot_json
    
    finput = urllib2.urlopen(historical) 
    json_string = finput.read() 
    parsed_json = json.loads(json_string)
    #print parsed_json
    
    # Observations for this day from the historical weather record
    obs = parsed_json['history']['observations']
    for o in range(0, len(obs)):
        print 'Weather in ' + city + ', ' + state
        year = obs[o]['date']['year']
        month = obs[o]['date']['mon']
        day = obs[o]['date']['mday']
        hour = obs[o]['date']['hour']
        minutes = obs[o]['date']['min']
        seconds = str('00')
        tzname = obs[o]['date']['tzname']
        conditions = obs[o]['conds']
        if (float(obs[o]['precipm']) <= 0): 
            precip = str(0)
        else: 
            precip = obs[o]['precipm']
        tempi = obs[o]['tempi']
        
        # Correct tz offset - need to generalize this function
        yyyymmddhhmm = year+month+day+hour+minutes
        tz_offset = '+0000' # default to UTC
        # Washington DC daylight savings start at 2012-03-11T02:00:00 and end at 2012-11-04T02:00:00
        if ((tzname == 'America/New_York') & (int(year) == 2012)):
            if ((int(yyyymmddhhmm) >= 201203110200) & (int(yyyymmddhhmm) < 201211040200)):
                tz_offset = '-0400'
            else:
                tz_offset = '-0500'
        # Arizona does not change time zone
        if (tzname == 'America/Arizona'):
            tz_offset = '-0700'
        iso_datetime = year + '-' + month + '-' + day + 'T' + hour + ':' + minutes + ':' + seconds + tz_offset
        
        # Print weather data to screen   
        print obs[o]['date']['pretty']
        print 'iso_datetime: ' + iso_datetime
        print 'Conditions: ' + conditions
        print 'Temperature(F): ' + tempi
        print 'Precipitation(in/hr): ' + precip
        print # empty line
        
        # Print weather data to file
        foutput.write(iso_datetime + ',' + tempi + ',' + precip + ',' + conditions + '\n')
    # end for o      
    
    calls = calls + 1
    
    if calls == max_calls:
        # Pause to stay within the API limits
        print 'Paused 60 secs due to API limits...'
        time.sleep(60)
        calls = 0   # reset api counter
        
    finput.close() # close the daily input file

# end for d
foutput.close() # close the outputfile

print 'Completed Historical Weather Retrieval...'
print 'Data written to file ' + weatherCityState + str(startdate) + '.csv'
