rx-weather - Fetch current weather conditions
=============================================

``rx-weather`` is a simple command line utility that allows the user
to retrieve current weather conditions based on zip code. It exists
primarily as an exercise in using python `Rx <https://github.com/ReactiveX/RxPY>`_
as well as the `requests <http://docs.python-requests.org/en/master/>`_ library.

Installation
------------

::

    pip install rx-weather

Depending on your local python environment, you may need to specify the 
python3 version of pip: 

::

    pip3 install gfb


Basic Usage
-----------

::

    usage: rx-weather [-h] [--just-temp] [--version] appid zip

    positional arguments:
      appid        open weather map api key
      zip          zip code for which to get the weather

    optional arguments:
     -h, --help   show this help message and exit
     --just-temp  return location and temperature only
     --version    show program's version number and exit

For example::

    rx-weather <your openweathermap app id here> 49002

Returns::

    Portage, US
    lat: 42.19 lon: -85.56
    sunrise: 7:41AM
    sunset: 6:12PM

    Temperature: 27.7°F
    Wind Speed:
            7.4mph at 336°
    Conditions:
            clear sky

Where as::

    rx-weather <your openweathermap app id here> 49002 --just-temp

Returns::

    Portage: 27.7°F

This result is suitable for displaying the current temperature in a utility
such as ``i3status`` or a ``tmux`` status bar.

``rx-weather`` requires you to provide an api key from `OpenWeatherMap.org 
<http://openweathermap.org>`_. There is no cost for an api key but it does
require you register.

The source for this project is available here
https://github.com/barnardn/rx_weather.git

Requirements
------------

``rx-weather`` does require python 3.6 or better.


