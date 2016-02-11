##
##				| | | |     (_)                    | |  | |          | | | |	
##				| | | |_ __  _  ___ ___  _ __ _ __ | |  | | ___  __ _| |_| |__   ___ _ __ 
##				| | | | '_ \| |/ __/ _ \| '__| '_ \| |/\| |/ _ \/ _` | __| '_ \ / _ \ '__|
##				| |_| | | | | | (_| (_) | |  | | | \  /\  /  __/ (_| | |_| | | |  __/ | 
##	 			 \___/|_| |_|_|\___\___/|_|  |_| |_|\/  \/ \___|\__,_|\__|_| |_|\___|_|
## 
##	Code by:
##			https://github.com/Craio/
##			https://github.com/pimoroni/unicorn-hat/		
##			https://github.com/ZeevG/python-forecast.io/
##
##	Check readme.md at https://github.com/Craio/RaspberryPi/blob/master/UnicornWeather/readme.md
##	for information on how to use this. Forgive my bad code please!


#!/usr/bin/env python

from random import randint
from PIL import Image
import unicornhat as unicorn
import forecastio, time, colorsys, signal, numpy


# set forecast.io api

#insert your own api key in these brackets eg "abcdef1234567890"
api_key = "" 
# set lng and lat of location (just the numbers) i.e
# lat = 55.8578
# lng = -4.2425
lat = 
lng = 

#rotate display to show pngs with direction of the pi power cable facing 'up' to space
unicorn.rotation(270)

imgcloud = Image.open('img/weather_cloud.png')
imgsun = Image.open('img/weather_sun.png')
imgmoon = Image.open('img/weather_moon.png')
imgrain = Image.open('img/weather_rain.png')
imgsnow = Image.open('img/weather_snow.png') # change this png to display snowflake - one day I'll do this
imgwind = Image.open('img/weather_wind-line.png') # this can be swapped for 'weather_wind-turbine' if desired
 
def weatherloop():

  # define current time
  currenttime = time.localtime()

  # set pixel brightness based on time of day
  def setBrightness(currenttime):
    currenthour = currenttime.tm_hour
    # if it's between 12pm and 9pm,
    # use lower brightness value
    if(currenthour < 12 or currenthour > 21):
      unicorn.brightness(0.05)
    else:
      unicorn.brightness(0.3)
  # set brightness for time of day
  setBrightness(currenttime)

  # define forecast function (shortens the need to type long name)
  forecast = forecastio.load_forecast(api_key, lat, lng)

  # defines current weather function and prints icon conditions and temperature to terminal
  current_weather = forecast.currently()
  print current_weather.icon
  print current_weather.temperature

  # if weather is cloudy, print cloud icon
  if current_weather.icon in ['partly-cloudy-day','partly-cloudy-night']:
      for o_x in range(int(imgcloud.size[0]/8)):
	for o_y in range(int(imgcloud.size[1]/8)):

		for x in range(8):
			for y in range(8):
				pixel = imgcloud.getpixel(((o_x*8)+y,(o_y*8)+x))
                                # uncomment line below to enable printing pixel information to console window
				#print(pixel)
				r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
				unicorn.set_pixel(x, y, r, g, b)
                unicorn.show()
                time.sleep(120)
                unicorn.clear()
      
  # if weather is sunny, print sun icon
  if current_weather.icon in ['clear-day']:
      for o_x in range(int(imgsun.size[0]/8)):
	for o_y in range(int(imgsun.size[1]/8)):

		for x in range(8):
			for y in range(8):
				pixel = imgsun.getpixel(((o_x*8)+y,(o_y*8)+x))
                                # uncomment line below to enable printing pixel information to console window
				#print(pixel)
				r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
                                unicorn.set_pixel(x, y, r, g, b)
                unicorn.show()
                time.sleep(120)
                unicorn.clear()


  # if weather is clear at night, print moon icon
  if current_weather.icon in ['clear-night']:
      for o_x in range(int(imgmoon.size[0]/8)):
	for o_y in range(int(imgmoon.size[1]/8)):

		for x in range(8):
			for y in range(8):
				pixel = imgmoon.getpixel(((o_x*8)+y,(o_y*8)+x))
                                # uncomment line below to enable printing pixel information to console window
				#print(pixel)
				r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
				unicorn.set_pixel(x, y, r, g, b)
                unicorn.show()
                time.sleep(120)
                unicorn.clear()


  # if weather is rainy, print rain animation
  if current_weather.icon in ['rain']:
      for o_x in range(int(imgrain.size[0]/8)):
	for o_y in range(int(imgrain.size[1]/8)):

		for x in range(8):
			for y in range(8):
				pixel = imgrain.getpixel(((o_x*8)+y,(o_y*8)+x))
                                # uncomment line below to enable printing pixel information to console window
				#print(pixel)
				r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
				unicorn.set_pixel(x, y, r, g, b)
                unicorn.show()
                time.sleep(120)
                unicorn.clear()


  # if weather is snowy, print snow animation
  if current_weather.icon in ['snow']:
      for o_x in range(int(imgsnow.size[0]/8)):
	for o_y in range(int(imgsnow.size[1]/8)):

		for x in range(8):
			for y in range(8):
				pixel = imgsnow.getpixel(((o_x*8)+y,(o_y*8)+x))
                                # uncomment line below to enable printing pixel information to console window
				#print(pixel)
				r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
				unicorn.set_pixel(x, y, r, g, b)
                unicorn.show()
                time.sleep(120)
                unicorn.clear()


  # if weather is windy, print wind icon
  if current_weather.icon in ['wind']:
      for o_x in range(int(imgwind.size[0]/8)):
	for o_y in range(int(imgwind.size[1]/8)):

                for x in range(8):
                        for y in range(8):
                                pixel = imgwind.getpixel(((o_x*8)+y,(o_y*8)+x))
                                # uncomment line below to enable printing pixel information to console window
                                #print(pixel)
                                r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
                                unicorn.set_pixel(x, y, r, g, b)
                unicorn.show()
                time.sleep(120)
                unicorn.clear()


while True:
  weatherloop()

