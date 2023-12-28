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
        state_code = request.form['state_code']
        data = weather_finder(city,state_code=state_code)
        print(data)
        if data is not None:
            #if true redirect to weather_displayer function
            
            return redirect(url_for('weather.weather_displayer',long=data[0],lat=data[1]))

        
        
    return render_template('weather/index.html')




def weather_finder(city,country_code="",state_code="",limit=1):
    API_key = "696ff3236cff2b889401a9a8d64c86c2"
    

        
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state_code},{country_code}&limit={limit}&appid={API_key}"
    response = requests.get(url)
    error = ""
    
    if response.status_code == 200:
        data = []
        data_list = response.json()

        # Access data 
        first_item = data_list[0]
        lat = first_item["lat"]
        long = first_item["lon"]

        data.append(lat)
        data.append(long)
        

    else:
        error = 'Error with HTTP response'
        flash(error)  
    return data

@bp.route('/display')
def weather_displayer():
    #instantly renders weather.html, and i display the code here
    long = request.args.get('long', 'No Data Available')
    lat = request.args.get('lat', 'No Data Available')

    print(lat,long)
    return render_template('weather/weather.html',long=long,lat=lat)

    
        
        
    
    
    