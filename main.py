import requests
import datetime
import os

date = datetime.datetime.now().strftime("%d/%m/%y")
time = datetime.datetime.now().strftime("%H:%M:%S")

EXERCISE = (input("What exercise did you do today? (Specify duration and/or distance for maximum accuracy) ")).title()

###TODO : Set up Nutrionix
# Documentation: https://docs.google.com/document/d/1_q-K-ObMTZvO0qUEAxROrN3bwMujwAN25sLHwJzliK0/edit#
HEADERS = {
    "x-app-id": os.environ.get("NUTRITIONIX_ID"),
    "x-app-key": os.environ.get("NUTRITIONIX_API_KEY"),
}

PARAS = {
    "query": EXERCISE,
    "gender": "female",
    "weight_kg": 51,
    "height_cm": 158,
    "age": 25,
}

response = requests.post(url="https://trackapi.nutritionix.com/v2/natural/exercise", json = PARAS, headers = HEADERS)
result = response.json()

"""Sample output of NUTRITIONIX result
{'exercises':
     [{'tag_id': 317,
       'user_input': 'ran',
       'duration_min': 31.08,
       'met': 9.8,
       'nf_calories': 258.9,
       'photo': {'highres': 'https://d2xdmhkmkbyw75.cloudfront.net/exercise/317_highres.jpg',
                 'thumb': 'https://d2xdmhkmkbyw75.cloudfront.net/exercise/317_thumb.jpg',
                 'is_user_uploaded': False},
       'compendium_code': 12050,
       'name': 'running',
       'description': None,
       'benefits': None}]}"""

###TODO: Retrieve data from Sheety
sheet_endpoint = os.environ.get("SHEETY_ENDPOINT")

###TODO: Log data into Sheety
for exercise in result["exercises"]:
    sheet_input = {
        "workout":{
            "date": date,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

###TODO: Authorisation/bearer
SHEETY_BEARER = os.environ.get("SHEETY_BEARER")
SHEETY_HEADERS = {
    "Authorization": f"Bearer {SHEETY_BEARER}",
}

sheet_response = requests.post(sheet_endpoint, json=sheet_input, headers=SHEETY_HEADERS).json()

print(f"Sheety Response: \n {sheet_response}")
