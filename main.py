import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv('.env')
APP_ID = os.getenv('APP_ID')
API_KEY = os.getenv('API_KEY')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

nutrition_parameters = {
    "query": input("Tell me which exercises you did today: ")
}

header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json",
}

nutrition_exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
response = requests.post(url=nutrition_exercise_endpoint, json=nutrition_parameters, headers=header)
data = response.json()

data_list = data["exercises"]

first_exercise = [value for(key, value) in data_list[0].items() if key == "name" or key == "duration_min"
                  or key == "nf_calories"]

second_exercise = [value for(key, value) in data_list[1].items() if key == "name" or key == "duration_min"
                   or key == "nf_calories"]

sheet_header = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

sheet_endpoint = os.getenv('sheet_endpoint')

date = datetime.now()
formatted_date = date.strftime("%Y/%m/%d")
formatted_time = date.time().strftime("%X")

for items in data["exercises"]:
    sheet_update = {
        "workout": {
            "date": formatted_date,
            "time": formatted_time,
            "exercise": items["name"].title(),
            "duration": items["duration_min"],
            "calories": items["nf_calories"]
        }
    }

    sheet_response = requests.post(url=sheet_endpoint, json=sheet_update, headers=sheet_header)
    print(sheet_response.text)

# for items in second_exercise:
#     sheet_update = {
#         "workout": {
#             "date": formatted_date,
#             "time": formatted_time,
#             "exercise": second_exercise[2].title(),
#             "duration": second_exercise[0],
#             "calories": second_exercise[1]
#         }
#     }

# date, time, exercise, duration, calories

# sheet_response = requests.post(url=sheet_endpoint, json=sheet_update, headers=sheet_header)
# print(sheet_response.json())


# sheet_response = requests.get(url=sheet_endpoint, headers=sheet_header)
# print(sheet_response.json())
