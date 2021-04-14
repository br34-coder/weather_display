# Simple python tool to retrieve weather station information and display it on an e-Paper display

import requests
import json

from ast import literal_eval

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gfx')
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
    
def get_graphic_rotation(input_str):
    g_rot = 0
    
    if input_str == "N":
        g_rot = -90
    elif input_str == "NNE":
        g_rot = -112
    elif input_str == "NE":
        g_rot = -135
    elif input_str == "ENE":
        g_rot = -157
    elif input_str == "E":
        g_rot = -180
    elif input_str == "ESE":
        g_rot = -202
    elif input_str == "SE":
        g_rot = -225
    elif input_str == "SSE":
        g_rot = -247
    elif input_str == "S":
        g_rot = -270
    elif input_str == "SSW":
        g_rot = 68
    elif input_str == "SW":
        g_rot = 45
    elif input_str == "WSW":
        g_rot = 22
    elif input_str == "W":
        g_rot = 0
    elif input_str == "WNW":
        g_rot = -23
    elif input_str == "NW":
        g_rot = -45
    elif input_str == "NNW":
        g_rot = -68
        
    return g_rot

# get the arguments and switch modes
# switch between text mode (t) and graphical mode (g)
mode = 'g'

# switch data source between test data (t) and live data (l)
data_source = 'l'

arguments = len(sys.argv) - 1
position = 1
while(arguments >= position):
    #print("Parameter %i: %s" %(position, sys.argv[position]))
    if sys.argv[position] == "--help":
        print("--text for text mode, --test for test mode, --help for help")
        sys.exit()
    elif sys.argv[position] == "--text":
        mode = 't'
    elif sys.argv[position] == "--test":
        data_source = 't'
    else:
        print("Wrong argument!")
        sys.exit()
    position = position + 1



try:
    # init the display and the used fonts
    epd = epd2in7.EPD()

    epd.init()
    epd.Clear(0xFF)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    font8 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 8)
    font12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    
    # init the API path
    api_file = open("api_path.txt")
    api_path = api_file.read().replace("\n", "")
    api_file.close()
    
    
    while True:
        Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        
        #print("h: " + str(epd.height) + ", w: " + str(epd.width))
        
        # retrieve
        if data_source == 't':  # use test data
            file = open("test_data.txt")
            data = literal_eval(file.read().replace("\n", ""))
            file.close()
        else:   # use live data
            data = get_data(api_path)
            # save current data as test data
            #file = open("test_data.txt", "w")
            #file.write(str(data))
            #file.close()

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
        
        if mode == 't': 
            draw.text((10, 25), "Temp. (C): "+ str(data["observations"][0]["metric"]["temp"]), font = font24, fill = 0)
            draw.text((10, 52), "Humidity (%): " + str(data["observations"][0]["humidity"]), font = font24, fill = 0)
            draw.text((10, 79), "Wind Sp. (km/h): " + str(data["observations"][0]["metric"]["windSpeed"]), font = font24, fill = 0)
            draw.text((10, 106), "Wind Dir.: " + convert_w_dir(int(data["observations"][0]["winddir"])), font = font24, fill = 0)
            draw.text((10, 132), "UV Index: " + str(data["observations"][0]["uv"]), font = font24, fill = 0)
        else:
            # load background image
            bmp = Image.open(os.path.join(picdir, 'bgs.bmp'))
            Himage.paste(bmp, (0,0))
            
            # Temperature
            temp = int(data["observations"][0]["metric"]["temp"])
            fill0, fill10, fill20, fill30 = 255, 255, 255, 255
            if temp > 0:
                fill0 = 0
            if temp > 10:
                fill10 = 0
            if temp > 20:
                fill20 = 0
            if temp > 30:
                fill30 = 0
            
            draw.rectangle((42, 90, 62, 110), fill = fill0, outline = 0)
            draw.rectangle((42, 70, 62, 90), fill = fill10, outline = 0)
            draw.rectangle((42, 50, 62, 70), fill = fill20, outline = 0)
            draw.rectangle((42, 30, 62, 50), fill = fill30, outline = 0)
            draw.text((36, 125), str(data["observations"][0]["metric"]["temp"]) + "°", font = font24, fill = 0)
            
            # Humidity
            draw.text((113, 57), str(data["observations"][0]["humidity"]) + "%", font = font18, fill = 0)
            
            # UV index
            draw.text((205, 40), str(data["observations"][0]["uv"]), font = font24, fill = 0)
            draw.text((233, 85), "UV", font = font12, fill = 0)
            
            # Wind
            draw.text((158, 127), str(data["observations"][0]["metric"]["windSpeed"]), font = font24, fill = 0)
            draw.text((158, 152), "km/h", font = font8, fill = 0)
            draw.text((220, 141), convert_w_dir(int(data["observations"][0]["winddir"])), font = font12, fill = 0)
            bmp = Image.open(os.path.join(picdir, 'arr.bmp'))
            Himage.paste(bmp.rotate(get_graphic_rotation(convert_w_dir(int(data["observations"][0]["winddir"]))), Image.NEAREST, expand = 1, fillcolor = (255,255,255)), (190,132))
        
        epd.display(epd.getbuffer(Himage))
        
        time.sleep(60)
        
except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")
    epd2in7.epdconfig.module_exit()
    exit()

