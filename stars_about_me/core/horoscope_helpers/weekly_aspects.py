import random

import requests
import json
from datetime import datetime, timedelta
import time  # Import time module for sleep


def weekly_aspects():
    now = datetime.now()
    year = now.year
    month = now.month

    # Calculate next 7 days' dates
    days_in_week = [now + timedelta(days=i) for i in range(7)]

    weekly_aspects_data = []  # To store all daily aspects as strings

    url = "https://json.freeastrologyapi.com/western/aspects"
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': '8fPlcXObXf9C7Pu8ly9d7axHMTKET2ib6uTIuxFP'
    }

    # Loop through the next 7 days
    for day in days_in_week:
        date = day.day
        month = day.month
        year = day.year

        # Prepare the payload with the current day’s date
        payload = json.dumps({
            "year": year,
            "month": month,
            "date": date,
            "hours": 12,
            "minutes": 0,
            "seconds": 0,
            "latitude": 42.6975,
            "longitude": 23.3242,
            "timezone": 2,
            "config": {
                "observation_point": "topocentric",
                "ayanamsha": "tropical",
                "language": "en",
                "exclude_planets": [
                    "Lilith",
                    "Chiron",
                    "Ceres",
                    "Vesta",
                    "Juno",
                    "Pallas"
                ],
                "allowed_aspects": [
                    "Conjunction",
                    "Trine",
                    "Square",
                    "Opposition",
                    "Sextile"
                ],
                "orb_values": {
                    "Conjunction": 3,
                    "Opposition": 5,
                    "Square": 5,
                    "Trine": 5,
                    "Sextile": 5,
                    "Semi-Sextile": 5,
                    "Quintile": 5,
                    "Septile": 5,
                    "Octile": 5,
                    "Novile": 5,
                    "Quincunx": 5,
                    "Sesquiquadrate": 5
                }
            }
        })

        # Retry logic in case of failure (e.g., Status Code 429)
        attempts = 0
        while attempts < 5:  # Retry up to 5 times
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                # Process response if successful
                response_json = response.json()
                if "output" in response_json:  # Check if 'output' exists in the response
                    aspects_str = f"Aspects for {day.strftime('%Y-%m-%d')}:\n"

                    # Get the list of aspects for the day
                    aspects_list = response_json["output"]

                    # Randomly pick 3 aspects (or fewer if there aren't enough)
                    random_aspects = random.sample(aspects_list, min(3, len(aspects_list)))

                    # Build the response string with the randomly selected aspects
                    for aspect in random_aspects:
                        aspects_str += f"- {aspect['planet_1']['en']} {aspect['aspect']['en']} {aspect['planet_2']['en']}\n"

                    # Append to the weekly aspects data
                    weekly_aspects_data.append(aspects_str)
                else:
                    weekly_aspects_data.append(f"No aspects found for {day.strftime('%Y-%m-%d')}")
                break  # Exit the loop if successful
            else:
                # If status code is not 200 (e.g., 429), retry after a delay
                attempts += 1
                print(
                    f"Failed to get aspects for {day.strftime('%Y-%m-%d')}, Status Code: {response.status_code}. Retrying... (Attempt {attempts}/5)")
                time.sleep(5)  # Wait for 5 seconds before retrying

        # If we've exhausted all retry attempts
        if attempts == 5:
            weekly_aspects_data.append(f"Failed to get aspects for {day.strftime('%Y-%m-%d')} after multiple attempts.")

    # Join all the aspect data into one string and return
    return "\n".join(weekly_aspects_data)

