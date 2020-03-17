[Docker Hub](https://hub.docker.com/)
# Where To Lunch ?

"Where To Lunch" is a Web application, to end the daily team discussions in the morning on the topic "where are we going today for lunch ?"


## How

### Basic Features
* Each day all users can vote for restaurants where they want to eat.
* Votes gets deleted daily at 12.30 after that you can vote for the next date.

An admin needs to create Users (as staff member, so they can log in).
Admin can give users the right to create/change/view Restaurants. User should have not more rights than this.
To vote you need to be logged in.
Admin should customize the application (more details below)


 ### Special Features
 * Weather Forecast for the current/next day.
	* Based on what time it is. (if it is after noon) 
	* Weather forecast is pulled from: [https://openweathermap.org/forecast5](https://openweathermap.org/forecast5)

*  Slack notifications from a slack app (default = UTC time)
	* Notifications at 11 am for: Users that have not voted yet. 
	* Notification at 15 pm if tomorrow is bad weather.

* Statistics: 
	* for the current vote status.
	* restaurant choices of the past.

* Absence calendar
	* Users can enter an absent if they know they are unavailable on a specific date or  period.

* You can customize specific things (only the admin can do this)
	* For slack notifications you need to add the "Bot User OAuth Access Token".
		* you need to enter the name of the slack channel that should get the notification too.
		* you can enter the Slack Member ID from a slack user to his profile, so the message is more personalized
	* To show the forecast you need to add an API key from: [https://openweathermap.org/](https://openweathermap.org/)
		* A free API Key is sufficient.
		* You need to enter a City.
			* You can find your city here [https://openweathermap.org/find?q=](https://openweathermap.org/find?q=)
				* if you found your city copy the name e.q London, Cologne....
	* You can change the title of the application.
	* You can change the background image.
	* You can change the timezone
	    * this effects the time you get Slack messages and the daily deletion of the votes
	    * find your timezone here: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
# Technologies

* [Django](https://www.djangoproject.com/)
* [Chartjs.org](https://www.chartjs.org/)

# Build and run locally
First we need to install [python](https://www.python.org/downloads/).
   
After that we need to Install [pip](https://pip.pypa.io/en/stable/installing/),
pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from [python.org](https://www.python.org/downloads/) or if you are working in a Virtual Environment created by virtualenv or pyvenv.

Now pip need to install all dependencies for the project.
```
pip install requirements.txt
```
After that we can run following command to start our application.
```
python3 manage.py runserver --settings=LightningLunch.local_settings

```
Our application can be accessed via: [`http://127.0.0.1:8000`](http://127.0.0.1:8000)

If you want to run your production environment with your locally code changes you need to run following commands

Take down old volume
```
docker-compose down -v
```
Build Images
```
SECRET_KEY=string DATABASE_NAME=name SQL_USER=name SQL_PASSWORD=pw docker-compose -f docker-compose.prod.yml up --build 
```
Migrate new database scheme
```
docker-compose -f docker-compose.prod.yml exec lunchapp python manage.py migrate --noinput
```
Collect all static files
```
docker-compose -f docker-compose.prod.yml exec lunchapp python manage.py collectstatic --no-input --clear
```
Create an admin
```
docker-compose -f docker-compose.prod.yml exec lunchapp python manage.py createsuperuser
```

Our application can be accessed via: [`http://localhost:1337/`](http://localhost:1337/)

## Endpoints
The application contains 2 Rest Endpoints.

1. /api/charts/votes 
    
    gives back all restaurant names that have votes. Including all supporters,
    Images from the supporters if they have one and the color of the restaurant so that the statistics can be in color
 
    
2. /api/charts/choices
    
    gives back all restaurants names with the number of times the restaurant won the
    voting and the color.

# Licences

Copyright (c) 2020 Pilarczyk Till

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
