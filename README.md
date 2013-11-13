Status Bar Weather
=========================

Sublime Text 3 package for displaying weather info in status bar

## Preview

![Preview] (https://github.com/lowliet/sublimetext-StatusBarWeather/raw/master/preview_small.png)

![Preview] (https://github.com/lowliet/sublimetext-StatusBarWeather/raw/master/preview.png)

--------------

## How to install

 - Clone or [download](https://github.com/lowliet/sublimetext-StatusBarWeather/archive/master.zip) git repo into your packages folder

Using [Package Control](http://wbond.net/sublime_packages/package_control):

 - Run “Package Control: Install Package” command, and find `StatusBarWeather` package

--------------

## Settings

	// Turn on / off debug logs shown on console window
	"debug": false,

	// City code from Yahoo Weather
	// Go to http://weather.yahoo.com/, find your city and click on 'Extended Forecast'
	// You may need to disable AdBlock / Ghostery, otherwise page won't display correctly
	// Check the address bar for city code, it should look like this
	// http://www.weather.com/weather/extended/ --> CODE <-- ?par=yahoo&(...)
	// After changing this value you need to restart sublime
	"code": "UKXX0085",

	// Temperature unit, either Fahrenheits or Celsius
	// After changing this value you need to restart sublime
	"unit": "C",

	// Formatting string to display weather
	// Available values are:
	// [Country], [City], [Text], [Temp], [Unit], [Sunrise], [Sunset], [Pressure], [Humidity]
	// Each value will be replaced with appropriate weather data, example:
	// In [City] the weather is [Text] ([Temp][Unit])
	"format": "[City], [Text], [Temp][Unit]"

--------------