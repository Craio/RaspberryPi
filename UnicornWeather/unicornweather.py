#!/usr/bin/env python

##
##				| | | |     (_)                    | |  | |          | | | |	
##				| | | |_ __  _  ___ ___  _ __ _ __ | |  | | ___  __ _| |_| |__   ___ _ __ 
##				| | | | '_ \| |/ __/ _ \| '__| '_ \| |/\| |/ _ \/ _` | __| '_ \ / _ \ '__|
##				| |_| | | | | | (_| (_) | |  | | | \  /\  /  __/ (_| | |_| | | |  __/ | 
##	 			 \___/|_| |_|_|\___\___/|_|  |_| |_|\/  \/ \___|\__,_|\__|_| |_|\___|_|
## 
##	Code by:
##			https://github.com/craio/
##			https://github.com/pimoroni/unicorn-hat/		
##			https://github.com/ZeevG/python-forecast.io/
##                      https://github.com/xabertum/UnicornHatScroll/
##                      https://github.com/topshed/UnicornHatScroll/
##
##
##	Check readme.md at https://github.com/Craio/RaspberryPi/blob/master/UnicornWeather/readme.md/
##	for information on how to use this. Forgive my bad code please!

from random import randint
from PIL import Image
from bitarray import bitarray
from time import ctime
import unicornhat as unicorn
import forecastio, time, colorsys, signal, numpy, itertools
from UHScroll_defs_lowercase import *


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
 

## Define weather conditions

def weathercond():

    # define forecast function (shortens the need to type long name)
    global forecast
    forecast = forecastio.load_forecast(api_key, lat, lng)

    # defines current weather function and prints icon conditions and temperature to terminal
    global current_weather
    current_weather = forecast.currently()
    print ctime()
    print current_weather.icon
    global new_temp
    new_temp = int(round(current_weather.temperature))
    print new_temp
    print ''
    #set new_temp to be a string for later
    global new_temp_s
    new_temp_s = str(new_temp)







## uhscroll.py information
## this code is from 
## https://github.com/xabertum/UnicornHatScroll 
## and
## https://github.com/topshed/UnicornHatScroll


flip = [7,6,5,4,3,2,1,0]

def show_letter(letter,colour,brightness): #displays a single letter on th UH
    unicorn.rotation(270)        
    for i in range(8):
        for j in range(8):
            if letter[j][i]:
                if colour == 'red':
                    unicorn.set_pixel(j,flip[i],brightness,0,0)
                elif colour == 'green':
                    unicorn.set_pixel(j,flip[i],0,brightness,0)
                elif colour == 'blue':
                    unicorn.set_pixel(j,flip[i],0,0,brightness)
                elif colour == 'white':
                    unicorn.set_pixel(j,flip[i],brightness,brightness,brightness)
                elif colour == 'pink':
                    unicorn.set_pixel(j,flip[i],brightness,52,179)
                elif colour == 'cyan':
                    unicorn.set_pixel(j,flip[i],0,brightness,brightness)
                elif colour == 'yellow':
                    unicorn.set_pixel(j,flip[i],brightness,brightness,0)
                elif colour == 'orange':
                    unicorn.set_pixel(j,flip[i],brightness,128,0)
            else:
                unicorn.set_pixel(j,flip[i],0,0,0)

    unicorn.show()

def scroll_letter(letter,colour,brightness,speed): # scrolls a single letter across the UH
    for i in range(8):
        for p in range(6):
            letter[i].insert(0,False)
    for s in range(14):
        show_letter(letter,colour,brightness)
        time.sleep(speed)
        for i in range(8):
            letter[i].pop(0)
            letter[i].append(0)

## scrolling is achieved by redrawing the letter with a column of the bitarray shifted to the left 
## and a new blank column added to the right
def scroll_word(word,colour,brightness,speed): # scrolls a word across the UH
    for s in range(len(word[0])):
        show_letter(word,colour,brightness)
        time.sleep(speed)
        for i in range(8):
            word[i].pop(0)
            word[i].append(0)

def make_word(words): # takes a list of chars and concats into a word by making one big bitarray
    bigword = [bitarray(''),bitarray(''), bitarray(''),bitarray(''), bitarray(''),bitarray(''), bitarray(''),bitarray('')]
    for w in range(len(words)):
        for i in range(len(words[w])):
            bigword[i] = bigword[i] + words[w][i]
    return bigword
    
def trim_letter(letter): #trims a char's bitarray so that it can be joined without too big a gap
    trim = []
    for c in range(len(letter)):
        trim.append(letter[c].copy())
    if letter not in super_wides:
        for i in range(8):
            if letter not in wides:
                trim[i].pop(0)
            trim[i].pop(0)
            trim[i].pop(5)
            if letter in narrows:
                trim[i].pop(0)
            if letter in super_narrow:
                trim[i].pop(0)
                
    return trim

def map_character(chr):
    if chr in mapping:
        return mapping[chr]
    else:
        return mapping['_']



def map_character_lowercase(chr):
    if chr in mapping_lowercase:
        return mapping_lowercase[chr]
    else:
                return mapping_lowercase['_']


def load_message_lowercase(message):
    unicorn_message = []
    message = '  ' + new_temp_s + message # pad the message with a couple of spaces so it starts on the right
    skip = 0
    for ch in (range(len(message))):
        #print message[ch]
        if skip != 0:
            skip-=1
        else:
            if message[ch] == '~':
                spec = message[ch+1] + message[ch+2] + message[ch+3] + message[ch+4] + message[ch+5]
                unicorn_message.append(trim_letter(map_character_lowercase(spec)))
                skip = 5
            else:
                unicorn_message.append(trim_letter(map_character_lowercase(message[ch])))
        
    return(unicorn_message)

def unicorn_scroll_lowercase(new_temp_s,text,colour,brightness,speed):
    #try:
    scroll_word(make_word(load_message_lowercase(text)),colour,brightness,speed)
    #except: 
        #print 'Enter unicorn_scroll(message,colour,brightness,speed) where '
        #print 'message is a string, colour is either red,white,blue,green,pink, yellow, orange or cyan'
        #print 'brightness is a integer 0-255 and speed is the time between chars'






## This code is from 
## https://github.com/Craio/RaspberryPi/tree/master/UnicornWeather
## and 
## https://github.com/pimoroni/unicorn-hat



def weatherloop():

  weathercond()

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
      unicorn.brightness(0.1)
  # set brightness for time of day
  setBrightness(currenttime)

## now we begin to start displaying the weather icon and displaying the temperature



  # if weather is cloudy, print cloud icon
  if current_weather.icon in ['partly-cloudy-day','partly-cloudy-night','cloudy','fog']:
      for o_x in range(int(imgcloud.size[0]/8)):
	for o_y in range(int(imgcloud.size[1]/8)):

		for x in range(8):
			for y in range(8):
				pixel = imgcloud.getpixel(((o_x*8)+y,(o_y*8)+x))
				r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
				unicorn.set_pixel(x, y, r, g, b)
                unicorn.show()
                time.sleep(60)
                unicorn.clear()

        if new_temp < 0:
            for _ in itertools.repeat(None, 4):
                unicorn_scroll_lowercase(new_temp_s,'~degrsc  ','blue',255,0.15)
                time.sleep(10)
        elif new_temp >= 0:
            for _ in itertools.repeat(None, 4):
                unicorn_scroll_lowercase(new_temp_s,'~degrsc  ','white',255,0.15)
                time.sleep(10)




  # if weather is sunny, print sun icon
  if current_weather.icon in ['clear-day']:
      for o_x in range(int(imgsun.size[0]/8)):
	for o_y in range(int(imgsun.size[1]/8)):

		for x in range(8):
			for y in range(8):
				pixel = imgsun.getpixel(((o_x*8)+y,(o_y*8)+x))
				r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
                                unicorn.set_pixel(x, y, r, g, b)
                unicorn.show()
                time.sleep(60)
                unicorn.clear()
                
        if new_temp < 0:
            for _ in itertools.repeat(None, 4):
                unicorn_scroll_lowercase(new_temp_s,'~degrsc  ','blue',255,0.15)
                time.sleep(10)
        elif new_temp >= 0:
            for _ in itertools.repeat(None, 4):
                unicorn_scroll_lowercase(new_temp_s,'~degrsc  ','white',255,0.15)
                time.sleep(10)




  # if weather is clear at night, print moon icon
  if current_weather.icon in ['clear-night']:
      for o_x in range(int(imgmoon.size[0]/8)):
	for o_y in range(int(imgmoon.size[1]/8)):

		for x in range(8):
			for y in range(8):
				pixel = imgmoon.getpixel(((o_x*8)+y,(o_y*8)+x))
				r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
				unicorn.set_pixel(x, y, r, g, b)
                unicorn.show()
                time.sleep(60)
                unicorn.clear()
        
        if new_temp < 0:
            for _ in itertools.repeat(None, 4):
                unicorn_scroll_lowercase(new_temp_s,'~degrsc  ','blue',255,0.15)
                time.sleep(10)
        elif new_temp >= 0:
            for _ in itertools.repeat(None, 4):
                unicorn_scroll_lowercase(new_temp_s,'~degrsc  ','white',255,0.15)
                time.sleep(10)




  # if weather is rainy, print rain animation
  if current_weather.icon in ['rain','thunderstorm']:
      for o_x in range(int(imgrain.size[0]/8)):
	for o_y in range(int(imgrain.size[1]/8)):

		for x in range(8):
			for y in range(8):
				pixel = imgrain.getpixel(((o_x*8)+y,(o_y*8)+x))
				r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
				unicorn.set_pixel(x, y, r, g, b)
                unicorn.show()
                time.sleep(60)
                unicorn.clear()

        if new_temp < 0:
            for _ in itertools.repeat(None, 4):
                unicorn_scroll_lowercase(new_temp_s,'~degrsc  ','blue',255,0.15)
                time.sleep(10)
        elif new_temp >= 0:
            for _ in itertools.repeat(None, 4):
                unicorn_scroll_lowercase(new_temp_s,'~degrsc  ','white',255,0.15)
                time.sleep(10)




  # if weather is snowy, print snow animation
  if current_weather.icon in ['snow','sleet','hail']:
      for o_x in range(int(imgsnow.size[0]/8)):
	for o_y in range(int(imgsnow.size[1]/8)):

		for x in range(8):
			for y in range(8):
				pixel = imgsnow.getpixel(((o_x*8)+y,(o_y*8)+x))
				r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
				unicorn.set_pixel(x, y, r, g, b)
                unicorn.show()
                time.sleep(60)
                unicorn.clear()

        if new_temp < 0:
            for _ in itertools.repeat(None, 4):
                unicorn_scroll_lowercase(new_temp_s,'~degrsc  ','blue',255,0.15)
                time.sleep(10)
        elif new_temp >= 0:
            for _ in itertools.repeat(None, 4):
                unicorn_scroll_lowercase(new_temp_s,'~degrsc  ','white',255,0.15)
                time.sleep(10)




  # if weather is windy, print wind icon
  if current_weather.icon in ['wind','tornado']:
      for o_x in range(int(imgwind.size[0]/8)):
	for o_y in range(int(imgwind.size[1]/8)):

                for x in range(8):
                        for y in range(8):
                                pixel = imgwind.getpixel(((o_x*8)+y,(o_y*8)+x))
                                r, g, b = int(pixel[0]),int(pixel[1]),int(pixel[2])
                                unicorn.set_pixel(x, y, r, g, b)
                unicorn.show()
                time.sleep(60)
                unicorn.clear()
                
        if new_temp < 0:
            for _ in itertools.repeat(None, 4):
                unicorn_scroll_lowercase(new_temp_s,'~degrsc  ','blue',255,0.15)
                time.sleep(10)
        elif new_temp >= 0:
            for _ in itertools.repeat(None, 4):
                unicorn_scroll_lowercase(new_temp_s,'~degrsc  ','white',255,0.15)
                time.sleep(10)




while True:
  weatherloop()
