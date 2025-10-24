import csv
import requests
import os
import json

#create requests object and get key
with open(os.path.dirname(os.getcwd()) + '/access_keys.txt') as json_file:
    keys = json.load(json_file)

#Create header object.
headers={
    'Authorization': "Bearer " + keys['prod']
}

API_URL = "https://cms.instructure.com/api/v1"

#session object creation
#Sessions allow for us to retain the correct headers across calls.

session = requests.Session()
session.headers.update(headers)

#Grading periods object. The grading periods call requires the name of the grading period as you modify the grading period, for some reason.
#We also have 3 seperate grading periods for our 3 calendars. Therefore we want to create an object for all of the grading periods. 
grading_periods = [{
    'id': '277',
    'name': '25-26 UNC Charlotte Early Colleges',
}, {
    'id': '278',
    'name': '25-26 CPCC Early/Middle Colleges',
}, {
    'id': '279',
    'name': '25-26 CMS Grading Period',
}]

terms = []
#get the whole csv file
#This file comes from the SIS Export Report from Canvas. Then it is edited to associate the correct grading period ID number with the terms.
#Our terms have the school name on them -- this is unfortunately a manual process to associate the correct IDs.

with open('terms.csv', 'r', encoding='utf-8-sig') as terms_file:
    csv_reader = csv.DictReader(terms_file) # Skip header row
    for row in csv_reader:
        terms.append(row)

#filter by grading periods
#This code will filter the terms by ID and then make the API call. You want to change the periods ONCE with the terms that need to go into the period.
for p in grading_periods:
    filtered_grading_periods = [str(t['canvas_term_id']) for t in terms if t['grading period'] == p['id']]
    #print(f"Filtered grading periods for {p}: {filtered_grading_periods}")
    #print(type(filtered_grading_periods))

    #These are the parameters that need to be sent to the API call.
    params = {
        'enrollment_term_ids': filtered_grading_periods,
        'grading_period_set': {
            'title': p['name'],
        }
    }
    #print(f'{API_URL}/accounts/1/grading_period_sets/{p["id"]}')  # Use p["id"] to access the id
    rep = session.patch(f'{API_URL}/accounts/1/grading_period_sets/{p["id"]}', json=params)
    print(rep)
