
# Simple python tool to retrieve weather station information and display it on an e-Paper display
# requires: requests, json
import requests
import json


# retrieve and transform the weather data as a dict
def get_data(link):
    # Retrieve the data as a JSON
    data_json = requests.get(link).text

    # Transform into a dict (actually a dict of list of dict of dict)
    data_dict = json.loads(data_json)

    return data_dict

# retrieve
data = get_data("https://api.weather.com/v2/pws/observations/current?stationId=ITALHE7&format=json&units=m&apiKey=6532d6454b8aa370768e63d6ba5a832e")

# Pretty print all data
#print(json.dumps(data, indent = 4, sort_keys=True))

# Print selected data
message = "Timestamp: " + data["observations"][0]["obsTimeLocal"] + "\n"
message += "Temperature (C): " + str(data["observations"][0]["metric"]["temp"]) + "\n"
message += "Humidity (%): " + str(data["observations"][0]["humidity"]) + "\n"
message += "Wind Speed (km/h): " + str(data["observations"][0]["metric"]["windSpeed"]) + "\n"
message += "Wind Direction (degree): " + str(data["observations"][0]["winddir"]) + "\n"
message += "UV Index: " + str(data["observations"][0]["uv"]) + "\n"

print(message)
