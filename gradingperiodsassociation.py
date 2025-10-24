import csv
import requests
import os
import json

#create requests object and get key
with open(os.path.dirname(os.getcwd()) + '/access_keys.txt') as json_file:
    keys = json.load(json_file)

headers={
    'Authorization': "Bearer " + keys['prod']
}

API_URL = "https://cms.instructure.com/api/v1"

#session object creation

session = requests.Session()
session.headers.update(headers)

# #test for 1 grading period
# #let's make the API call
# params = {
#     'enrollment_term_ids': ['3689'],
#     'grading_period_set': {
#         'title': '25-26 UNC Charlotte Early Colleges',
#     }
# }
# print(f'{API_URL}/accounts/1/grading_period_sets/277')  # Use p["id"] to access the id
# rep = session.patch(f'{API_URL}/accounts/1/grading_period_sets/277', json=params) 
# print(rep)



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
with open('terms.csv', 'r', encoding='utf-8-sig') as terms_file:
    csv_reader = csv.DictReader(terms_file)# Skip header row
    for row in csv_reader:
        terms.append(row)

#filter by grading periods
for p in grading_periods:
    filtered_grading_periods = [str(t['canvas_term_id']) for t in terms if t['grading period'] == p['id']]
    #print(f"Filtered grading periods for {p}: {filtered_grading_periods}")
    print(type(filtered_grading_periods))
    #let's make the API call
    params = {
        'enrollment_term_ids': filtered_grading_periods,
        'grading_period_set': {
            'title': p['name'],
        }
    }
    print(f'{API_URL}/accounts/1/grading_period_sets/{p["id"]}')  # Use p["id"] to access the id
    rep = session.patch(f'{API_URL}/accounts/1/grading_period_sets/{p["id"]}', json=params)
    print(rep)
