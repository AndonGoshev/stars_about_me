# import requests
# import json
#
# url = "https://json.freeastrologyapi.com/western/aspects"
#
# payload = json.dumps({
#   "year": 2025,
#   "month": 4,
#   "date": 18,
#   "hours": 10,
#   "minutes": 30,
#   "seconds": 0,
#   "latitude": 17.38405,
#   "longitude": 78.45636,
#   "timezone": 5.5,
#   "config": {
#     "observation_point": "topocentric",
#     "ayanamsha": "tropical",
#     "language": "en",
#     "exclude_planets": [
#       "Lilith",
#       "Chiron",
#       "Ceres",
#       "Vesta",
#       "Juno",
#       "Pallas"
#     ],
#     "allowed_aspects": [
#       "Conjunction",
#       "Trine"
#     ],
#     "orb_values": {
#       "Conjunction": 3,
#       "Opposition": 5,
#       "Square": 5,
#       "Trine": 5,
#       "Sextile": 5,
#       "Semi-Sextile": 5,
#       "Quintile": 5,
#       "Septile": 5,
#       "Octile": 5,
#       "Novile": 5,
#       "Quincunx": 5,
#       "Sesquiquadrate": 5
#     }
#   }
# })
# headers = {
#   'Content-Type': 'application/json',
#   'x-api-key': '8fPlcXObXf9C7Pu8ly9d7axHMTKET2ib6uTIuxFP'
# }
#
# response = requests.request("POST", url, headers=headers, data=payload)
#
# print(response.text)