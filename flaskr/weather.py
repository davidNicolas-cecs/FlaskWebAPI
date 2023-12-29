import json
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests


bp = Blueprint('weather', __name__)

@bp.route('/',methods=('GET','POST'))
@bp.route('/home', methods = ('GET','POST'))
def index():
    data=None
    db=get_db
    if request.method == 'POST':
        city = request.form['city']
        #everytime we search something that gets a hit, we send it to the database
        state_code = request.form['state_code']
        data = geocoding(city,state_code=state_code)
        if data is not None:
            print("DATA IS:",data)
            #0 - name, 1 - temp, 2 - feels like, 3 - pressure, 4 - humidity
            #if true redirect to weather_displayer function
            
            return redirect(url_for('weather.weather_displayer', name=data[0], temp=data[1], feels_like=data[2], pressure=data[3], humidity=data[4]))

        
        
    return render_template('weather/index.html')




def geocoding(city,country_code="",state_code="",limit=1):
    API_key = "696ff3236cff2b889401a9a8d64c86c2"    
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state_code},{country_code}&limit={limit}&appid={API_key}"
    response = requests.get(url)
    error = ""
    
    if response.status_code == 200:
        data = []
        data_list = response.json()

        # Access data 
        first_item = data_list[0]
        name = first_item['name']
        lat = first_item["lat"]
        long = first_item["lon"]
        data.append(name)
        current_weather(lat,long,API_key,data)


    else:
        error = 'Error with HTTP response'
        flash(error)  
    return data

@bp.route('/display')
def weather_displayer():
    #instantly renders weather.html, and i display the code here
    name = request.args.get('name', 'No Data Available')
    temp = request.args.get('temp', 'No Data Available')
    feels_like = request.args.get('feels_like', 'No Data Available')
    pressure = request.args.get('temp', 'No Data Available')
    humidity = request.args.get('humidity', 'No Data Available')
    
    
    
    
    return render_template('weather/weather.html',name=name, temp=temp, feels_like=feels_like, pressure=pressure,humidity=humidity)

    
def current_weather(lat,lon,API_key,data):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Successfully made a request to openweathermap")
        print(response.content)
        data_list = response.json()
        main = data_list['main']
        print(main)
        #get all relevent data
        temp,feels_like,pressure,humidity = main['temp'],main['feels_like'], main['pressure'], main['humidity']
        data.append(temp)
        data.append(feels_like)
        data.append(pressure)
        data.append(humidity)
    
        
    
@bp.route('/searches', methods = ('GET', 'POST'))
def searches():
    return render_template('weather/recent.html')