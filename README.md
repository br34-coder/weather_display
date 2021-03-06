# weather_display
A simple project to display the current weather on a e-Paper display using the Raspberry Pi Zero

## Hardware setup
The setup used in this project consists of
1. A Raspberry PI Zero W v1.1
2. A Waveshare 2.7inch e-Paper HAT Rev2.1

## Software setup
Base OS: Raspbian OS full (Linux raspberrypi 5.10.17+ #1403 Mon Feb 22 11:26:13 GMT 2021 armv6l GNU/Linux)

### Enable SPI interface
1. Open a terminal and run `sudo raspi-config`
2. In the menu, navigate to "Interface Options" -> "SPI" and enable the SPI interface
3. Reboot your PI: `sudo reboot`

### Install BCM2835 libraries
In a terminal, execute the following:
```
wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.60.tar.gz
tar zxvf bcm2835-1.60.tar.gz
cd bcm2835-1.60/
sudo ./configure
sudo make
sudo make check
sudo make install
```

### Install wiringPI
In a terminal, execute the following:
`sudo apt-get install wiringpi`

### Install the python libraries (python3)
In a terminal, execute the follwing:
```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
sudo pip3 install spidev
```

### Copy in the library
In a separate folder, clone the example project repo from waveshare: `git clone https://github.com/waveshare/e-Paper`
Copy the `pic` and the `lib` folder from `e-Paper/RaspberryPi_JetsonNano/python`over to the root of your project folder

## How to run it
1. Clone the repo to your Raspberry PI
2. Open a terminal and navigate into the root folder of the project (where main.py is)
3. Run `sudo python3 main.py`

List of arguments:
- `--help` for list of arguments
- `--test` for using test data instead of real data from the API
- `--text` for using text-based output rather than graphical output

## How to change the weather station
In this project I am fetching the data of the weather station in my garden. If you want to change the station, you simply have to change the station code in the URL within the `api_path.txt` file.
Currently, it looks like this:
`https://api.weather.com/v2/pws/observations/current?stationId=ITALHE7&format=json&units=m&apiKey=6532d6454b8aa370768e63d6ba5a832e`
The station code within this URL is "ITALHE7". Simply replace this with the station code of the weather station you want to be displayed. 
