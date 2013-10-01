#!/usr/bin/python
#
# Gather historical weather data using the weatherunderground API
#

import urllib2 
import json 

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

## Open file for writing
foutput = open('precipWashingtonDC.csv','w')

## Historical Data
prefix_key = 'http://api.wunderground.com/api/34e4d065c41d49d4/history_'
start_date = 20120301
numdays = 11
query = '/q/'
state = 'DC'
city = 'Washington'
json_end = '.json'

for d in range(0, numdays):
    date = str(start_date + d)
    
    historical = prefix_key + date  + query + state + '/' + city + json_end
    
    finput = urllib2.urlopen(historical) 
    json_string = finput.read() 
    parsed_json = json.loads(json_string)
    #print parsed_json
    
#     # Date from Header Information
#     date_pretty = parsed_json['history']['date']['pretty']
#     year = parsed_json['history']['date']['year']
#     month = parsed_json['history']['date']['mon']
#     day = parsed_json['history']['date']['mday']
#     hour = parsed_json['history']['date']['hour']
#     minutes = parsed_json['history']['date']['min']
#     seconds = str('00')
#     print date_pretty
#     print year + '-' + month + '-' + day + 'T' + hour + ':' + minutes + ':' + seconds 
    
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
        
        # Correct tz offset for daylight savings start at 2012-03-11T02:00:00 and end at 2012-11-04T02:00:00
        yyyymmddhhmm = year+month+day+hour+minutes
        tz_offset = '+0000' # default to UTC
        if ((tzname == 'America/New_York') & (int(year) == 2012)):
            if ((int(yyyymmddhhmm) >= 201203110200) & (int(yyyymmddhhmm) < 201211040200)):
                tz_offset = '-0400'
            else:
                tz_offset = '-0500'
        iso_datetime = year + '-' + month + '-' + day + 'T' + hour + ':' + minutes + ':' + seconds + tz_offset
        
        # Print weather data to screen   
        print obs[o]['date']['pretty']
        print 'iso_datetime: ' + iso_datetime
        print 'Conditions: ' + obs[o]['conds']
        print 'Temperature(F): ' + obs[o]['tempi']
        if (float(obs[o]['precipm']) <= 0): 
            precip = str(0)
        else: 
            precip = obs[o]['precipm']
        print 'Precipitation(in/hr): ' + precip
        print # empty line
        
        # Print weather data to file
        foutput.write(iso_datetime + ',' + precip + '\n')
    
    # end for o      
    finput.close() # close the daily input file

# end for d
foutput.close() # close the outputfile

# Read more at http://www.wunderground.com/weather/api/d/docs?d=resources/code-samples#T43sEjcDrJbDoyIo.99