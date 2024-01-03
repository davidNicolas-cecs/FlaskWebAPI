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
    '''
    Description:
    -------------
    Function presents the weather page, inserts data into the db if the user is logged in
    
    Gets: data from openweatherapi
    
    Returns: data as a list
    '''
    data=None
    db = get_db()
    error = None
    
    if request.method == 'POST':
        #take data from 'index.html
        city = request.form['city']  
        state_code = request.form['state_code']
        country_code = request.form['country_code']
        
        #requested data
        want_humidity = request.form.get('humidity') # returns string
        want_pressure = request.form.get('pressure')
        want_feels_like = request.form.get('feels_like')
        print(f"Humidity is {want_humidity}, pressure is {want_pressure}, feels like is {want_feels_like}")
        
        #Checks if all the values entered are correct, if not, redirect back to home
        if not checkValues(city,state_code,country_code):
            print("Invalid request forms, redirecting back to home page---")
            return redirect(url_for('weather.index'))
            
        #try getting lat and lon from info
        try: 
            data = geocoding(city,state_code,country_code,want_humidity,want_pressure,want_feels_like)
        except:
            flash("Could not find the location, Please try again.")
            return redirect(url_for("weather.index"))
        if data is not None:
            #0 - name, 1 - temp, 2 - feels like, 3 - pressure, 4 - humidity
            #if true redirect to weather_displayer function           
            #submit data into the database
            if g.user:
                #if the user is a logged in
                # Get the user ID based on the username
                try:
                    user_id_query = f"SELECT id FROM user WHERE username = '{g.user['username']}'"
                    user_id_result = db.execute(user_id_query)
                    user_id = user_id_result.fetchone()[0] if user_id_result else None
                except:
                    flash("Error retrieving recent searches")
                    return redirect(url_for('weather.index'))
                if user_id: # if a user is found
                    # Create the parameterized SQL query
                    search_insert_query = "INSERT INTO searches (user_id, search_name) VALUES (?, ?)"
                    name = str(data[0])
                    # Execute the query with parameters
                    db.execute(search_insert_query, (user_id, name))
                    db.commit()
                    
            return redirect(url_for('weather.weather_displayer', name=data[0], temp=data[1], feels_like=data[2], pressure=data[3], humidity=data[4]))
        else:
            error = "The search location could not be found"
            flash(error)
            return redirect(url_for('weather.index'))
    return render_template('weather/index.html')

def checkValues(city,state_code,country_code):
    '''
    Description:
    -------------
    Function validates the user input from index.html
    
    Gets: data from index.html and verifys that it is in correct format
    
    Returns: true or false
    '''
    #returns false if a value is incorrect
    error = "Invalid format"
    if city.isalpha() and (len(state_code)) < 4 and (state_code.isalpha or state_code == "" ) and len(country_code) < 7:
        return True   
    flash(error)
    return False



def geocoding(city,state_code,country_code,want_humidity,want_pressure,want_feels_like):
    '''
    Description:
    -------------
    Function gets the geolocation of the request in order to redirect to get current weather
    
    Gets: data from openweatherapi (lat, long)
    
    Returns: data as a list or false if location not found
    '''
    limit=1
    API_key = "696ff3236cff2b889401a9a8d64c86c2"    
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state_code},{country_code}&limit={limit}&appid={API_key}"
    response = requests.get(url)
    error = ""
    data = []
    if response.status_code == 200:
        data_list = response.json() #get data from response
        # Access data 
        first_item = data_list[0]
        name = first_item['name']
        lat = first_item["lat"]
        lon = first_item["lon"]
        data.append(name)
        current_weather(lat,lon,API_key,data,want_humidity,want_pressure,want_feels_like)
    else:
        error = f'Could not find the location{response.status_code}'
        flash(error)  
        return False
    return data

@bp.route('/display')
def weather_displayer():
    '''
    Description:
    -------------
    Function presents the weather from the data recieved and displays in html
    
    Gets: data from functions "weather_geolocation" and "weather_current_location
    
    Returns: html display
    '''
    #instantly renders weather.html, and display the data
    name = request.args.get('name', 'No Data Available')
    temp = request.args.get('temp', 'No Data Available')
    feels_like = request.args.get('feels_like', 'No Data Available')
    pressure = request.args.get('pressure', 'No Data Available')
    humidity = request.args.get('humidity', 'No Data Available')
    return render_template('weather/weather.html',name=name, temp=temp, feels_like=feels_like, pressure=pressure,humidity=humidity)

    
def current_weather(lat,lon,API_key,data,want_humidity,want_pressure,want_feels_like):
    '''
    Description:
    -------------
    Function gets the current weather from the geolocations provided 
    
    Gets: data from openweatherapi (temp, feels_like, humidity, pressure) as well as user requested data
    
    Returns: data as a list with the specified users requested data only
    '''
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial&appid={API_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Successfully made a request to openweathermap")
        data_list = response.json()
        main = data_list['main']
        #get all relevent data
        temp,feels_like,pressure,humidity = main['temp'],main['feels_like'], main['pressure'], main['humidity']
        
        data.append(temp)
        
        print("CHECKING BOXES ON USER WANTS")
        
        if want_feels_like == 'on':
            print("we want feels like")
            data.append(feels_like)
        else:
            print("we dont want feels like")
            data.append('off')
            
        if want_pressure == 'on':
            print('we want pressure')
            data.append(pressure)
        else:
            print('we dont want pressure')
            data.append('off')
        if want_humidity == 'on':
            print('we want humidity')
            data.append(humidity)
        else:
            print('we dont want humidity')
            data.append('off')       
            
        print(data)
    
        
    
@bp.route('/searches', methods = ('GET', 'POST'))
def searches():
    '''
    Description:
    -------------
    Function presents the weather with information from request
    
    Gets: data from "weather.current_weather"
    
    Returns: html display with data
    '''
    return render_template('weather/recent.html')