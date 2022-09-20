import os
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

MY_GENDER = "male"
MY_AGE = 37
MY_WEIGHT_KG = 89
MY_HEIGHT_CM = 177

NUTRITIONIX_API_KEY = os.environ['NUTRITIONIX_API_KEY']
NUTRITIONIX_APPLICATION_ID = os.environ['NUTRITIONIX_APPLICATION_ID']

NUTRITIONIX_URL = "https://trackapi.nutritionix.com/v2/natural/exercise"
NUTRITIONIX_REQUEST_PARAMS = {
    "query": input("What exercises did you do today? "),
    "gender": MY_GENDER,
    "weight_kg": MY_WEIGHT_KG,
    "height_cm": MY_HEIGHT_CM,
    "age": MY_AGE
}
NUTRITIONIX_HEADERS = {
    "x-app-id": NUTRITIONIX_APPLICATION_ID,
    "x-app-key": NUTRITIONIX_API_KEY
}

SHEETY_URL = os.environ['SHEETY_URL']
SHEETY_USERNAME = os.environ['SHEETY_USERNAME']
SHEETY_PASSWORD = os.environ['SHEETY_PASSWORD']
basic = HTTPBasicAuth(SHEETY_USERNAME, SHEETY_PASSWORD)
nutritionix_response = None


def get_calculation_from_nutritionix():
    response = requests.post(url=NUTRITIONIX_URL, json=NUTRITIONIX_REQUEST_PARAMS,
                             headers=NUTRITIONIX_HEADERS)
    if response.status_code != 200:
        print("There was an error communicating with Nutritionix.")
    else:
        global nutritionix_response
        nutritionix_response = response.json()


def make_posts_to_sheety():
    global nutritionix_response
    if len(nutritionix_response["exercises"]) == 0:
        print("Nutritionix couldn't understand your input. Nothing recorded.")
    else:
        for i in nutritionix_response["exercises"]:
            sheety_add_new_row = {
                "workout":
                    {
                        "date": datetime.now().strftime("%d/%m/%Y"),
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "exercise": i["name"].title(),
                        "duration": i["duration_min"],
                        "calories": i["nf_calories"]
                    }
            }
            response = requests.post(url=SHEETY_URL, json=sheety_add_new_row, auth=basic)
            if response.status_code != 200:
                print("Communication error with Sheety. '{}' not recorded.".format(i["name"].title()))
            else:
                print("'{}' successfully recorded.".format(i["name"].title()))


get_calculation_from_nutritionix()
make_posts_to_sheety()

# This code runs on replit
