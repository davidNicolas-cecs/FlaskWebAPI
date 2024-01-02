# 🌞 FlaskWebAPI
## Table of Contents
1. [Purpose](#💻purpose)
2. [Features](#🌄features)
3. [Installation](#installation)
4. [Usage](#🌍usage)
6. [Endpoints](#🌌endpoints)



## 💻Purpose

A lightweight python web application in Flask that allows a user to request weather data from a given location. 


## 🌄Features

* Registration and Login 
* Pick and chose what information you recieve
* Logged in Users get the ability to recall past searches
* Light-weight database

## 🌍Usage:
To use the application, city name must be provided, state code (only applicable for US states), and country code. 

You are then allowed to chose what information you want the website to display about the location requested, (i.e only tempature? or tempature and humidity, etc)

The website is only intended to search for the current weather of a given location. 

## 🌌Endpoints 

The endpoints the application calls on openweathermap are 
* http://api.openweathermap.org/geo/1.0/direct
* https://api.openweathermap.org/data/2.5/weather


