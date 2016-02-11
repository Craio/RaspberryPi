UnicornWeather
=============
This python script will display the current weather status by means of an icon on your UnicornHAT, a Raspberry Pi attachment. This information is pulled from [Forecast.io](https://forecast.io/).

Installation
-------
To install the UnicornHAT Library you'll want to use the following commands (Check [here](https://github.com/pimoroni/unicorn-hat) if outdated):

```bash
\curl -sS get.pimoroni.com/unicornhat | bash
```
You'll then want to install ZeevG's python wrapper for the forecast.io API (Check [here](https://github.com/ZeevG/python-forecast.io) if outdated):

````bash
install pip install python-forecastio
````


Usage
-------
(Just as a note before we get started, check out [ZeevG's ReadMe](https://github.com/ZeevG/python-forecast.io) here for a more detailed explanation of how their project is used and how this integrates with UnicornWeather)

---

In order to use this script you will need a free [Forecast.io Developer account](https://developer.forecast.io/) and the longitude and latitude of the location you are interested in gathering weather information.

You can find the longitude and latitude from the Forecast.io website by searching for your location and taking note of the URL.

For Example:

The URL for Glasgow, Scotland would be `https://forecast.io/#/f/55.8578,-4.2425`

The part we are interested in would be `55.8578,-4.2425`

Where `55.8578` is the longitude and `-4.2425` is the latitude. These values are set to the `lat` and `lng` variables within the script respectfully.


---

The images called by this script are just regular 8 pixels by 8 pixels, you can modify these to display anything you'd like. 


---

Once you have set up your API Key and have your longitude and latitude in the script you can now run it! Open your terminal and change directories to where the script is located, then use the following command to show the current weather status on your bright LED display!
````bash
sudo python unicornweather.py
````


Additional notes
-------
Although this is commented within the script I've added this here just for sake of clarity.

You can change the brightness by modifying the numbers in the `unicorn.brightness()` below to your needs.

````python
  # set pixel brightness based on time of day
  def setBrightness(currenttime):
    currenthour = currenttime.tm_hour
    # if it's between 12 pm and 9 pm,
    # use lower brightness value
    if(currenthour < 12 or currenthour > 21):
      unicorn.brightness(0.05)
    else:
      unicorn.brightness(0.3)
  # set brightness for time of day
  setBrightness(currenttime)
````

---

Another note, a free Forecast.io developer account will only allow for 1000 calls per day without cost. In order to stay under this limit it is important to make sure the numbers given in `time.sleep()` will not cause the script to call for information too often.

Currently the script is set to call information every 120 seconds or every two minutes, this means the script will make a total of 720 calls per day falling well below the free 1000 limit.

Credits
-------
[Pimoroni](https://pimoroni.com/) for writing the [Library for UnicornHAT](https://github.com/pimoroni/unicorn-hat) and providing excellent examples on how to use this awesome little device!

GitHub user [ZeevG](https://github.com/ZeevG/) for writing the](https://github.com/ZeevG/python-forecast.io)

[Forecast.io](http://forecast.io) for providing an easy to use API and for having a pretty cool website too! 

I guess some to [me](https://github.com/Craio/) but really all the hard work was done by the people above!

License
-------
I'm not super keen on crazy license restrictions and limitations, you can do whatever you want with this project, go nuts!