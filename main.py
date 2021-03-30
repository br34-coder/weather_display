# Simple python tool to retrieve weather station information and display it on an e-Paper display

import requests
import json

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


from waveshare_epd import epd2in7
import time
from PIL import Image,ImageDraw,ImageFont
import traceback



# retrieve and transform the weather data as a dict
def get_data(link):
    # Retrieve the data as a JSON
    data_json = requests.get(link).text

    # Transform into a dict (actually a dict of list of dict of dict)
    data_dict = json.loads(data_json)

    return data_dict
    
# convert wind direction from degree to text
def convert_w_dir(w_dir):
    w_dir_str = "none"

    if w_dir > 11 and w_dir <= 33:
        w_dir_str = "NNE"
    elif w_dir > 33 and w_dir <= 56:
        w_dir_str = "NE"
    elif w_dir > 56 and w_dir <= 78:
        w_dir_str = "ENE"
    elif w_dir > 78 and w_dir <= 101:
        w_dir_str = "E"
    elif w_dir > 101 and w_dir <= 123:
        w_dir_str = "ESE"
    elif w_dir > 123 and w_dir <= 146:
        w_dir_str = "SE"
    elif w_dir > 146 and w_dir <= 168:
        w_dir_str = "SSE"
    elif w_dir > 168 and w_dir <= 191:
        w_dir_str = "S"
    elif w_dir > 191 and w_dir <= 213:
        w_dir_str = "SSW"
    elif w_dir > 213 and w_dir <= 236:
        w_dir_str = "SW"   
    elif w_dir > 236 and w_dir <= 258:
        w_dir_str = "WSW"
    elif w_dir > 258 and w_dir <= 281:
        w_dir_str = "W"
    elif w_dir > 281 and w_dir <= 303:
        w_dir_str = "WNW"
    elif w_dir > 303 and w_dir <= 326:
        w_dir_str = "NW"
    elif w_dir > 326 and w_dir <= 348:
        w_dir_str = "NNW"
    elif w_dir > 348 or w_dir <= 11:
        w_dir_str = "N"
        
    return w_dir_str



try:
   
    epd = epd2in7.EPD()

    epd.init()
    epd.Clear(0xFF)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    
    
    
    while True:
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        
        # retrieve
        data = get_data("https://api.weather.com/v2/pws/observations/current?stationId=ITALHE7&format=json&units=m&apiKey=6532d6454b8aa370768e63d6ba5a832e")

        # Print selected data
        message = "Timestamp: " + data["observations"][0]["obsTimeLocal"] + "\n"
        message += "Temperature (C): " + str(data["observations"][0]["metric"]["temp"]) + "\n"
        message += "Humidity (%): " + str(data["observations"][0]["humidity"]) + "\n"
        message += "Wind Speed (km/h): " + str(data["observations"][0]["metric"]["windSpeed"]) + "\n"
        message += "Wind Direction (degree): " + str(data["observations"][0]["winddir"]) + "\n"
        message += "UV Index: " + str(data["observations"][0]["uv"]) + "\n"
        print(message)
    
        # Show on display
        draw.text((10, 0), data["observations"][0]["obsTimeLocal"], font = font18, fill = 0)
        draw.line((0, 20, 264, 20), fill = 0)
        draw.text((10, 25), "Temp. (C): "+ str(data["observations"][0]["metric"]["temp"]), font = font24, fill = 0)
        draw.text((10, 52), "Humidity (%): " + str(data["observations"][0]["humidity"]), font = font24, fill = 0)
        draw.text((10, 79), "Wind Sp. (km/h): " + str(data["observations"][0]["metric"]["windSpeed"]), font = font24, fill = 0)
        draw.text((10, 106), "Wind Dir.: " + convert_w_dir(int(data["observations"][0]["winddir"])), font = font24, fill = 0)
        draw.text((10, 132), "UV Index: " + str(data["observations"][0]["uv"]), font = font24, fill = 0)
        epd.display(epd.getbuffer(Himage))
        
        time.sleep(60)
        
except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")
    epd2in7.epdconfig.module_exit()
    exit()

