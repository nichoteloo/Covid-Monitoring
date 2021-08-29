import yaml
import helper
import plotly
import requests
import mysql.connector
from flask import Markup
from plotly.graph_objs import Scatter, Layout

db = yaml.safe_load(open("config/" + 'db.yaml'))

################# Helper Function ########################
## Connect to MySQL
def MySQLConnect():
	mydb = mysql.connector.connect(
		host = db['mysql_host'],
		user = db['mysql_user'],
		password = db['mysql_password'],
		database = db['mysql_db'],
	)
	return mydb

## Call API
def callApi(route):
	response = requests.get(helper.BASE_URL + route).json()
	return response

## Get Country Summary
def getSummary(country):
	mydb = MySQLConnect()
	cur = mydb.cursor()

	query = "SELECT TotalConfirmed,TotalDeaths,TotalRecovered FROM dailysummary WHERE Country=(%s);"
	cur.execute(query,(country,))

	summary = cur.fetchall()
	mydb.close()
	
	return summary

## Get All Countries
def getCountries():
    mydb = MySQLConnect()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM countries")
    countries = cur.fetchall()
    mydb.close()
    return countries

## Option All Country
def getOptionCountries():
	option = ''

	countries = getCountries()
	for country in countries:
		option += "<option value='"+ str(country[0]).lstrip().replace(" ","-") +"'>"+ str(country[0]).lstrip() +"</option>"
	optionHTML = Markup(option)

	return optionHTML

## Get Slug Country
def getSlugCountry(country):
	mydb = MySQLConnect()
	cur = mydb.cursor()

	query = "SELECT (Slug) FROM countries WHERE Country=(%s);"
	cur.execute(query,(country,))

	slug = cur.fetchall()
	mydb.close()

	return slug

## Prepare Data Plotting
def preparePlotting(queryList):
	dataDictionary = {
		"X": [],
		"Y": [],
	}
	previousDay = ""
	for x in queryList:
		if (previousDay != ""):
			dataDictionary["X"].append(x[0] - previousDay[0])
		else:
			dataDictionary["X"].append(x[0])
		dataDictionary["Y"].append(x[1])
		previousDay = x
	return dataDictionary

## Example plot by pyplot
def examplePlot():
    plotly.offline.plot({
        "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
        "layout": Layout(title="hello world")
    })

def buildPlot(dataX, dataY, country, dataType, chartType):
	lineColor = "#498efc"

	if dataType == "Deaths":
		lineColor = 'PaleVioletRed'

	elif dataType == "Recovered":
		lineColor = "#ff9900"

	if chartType == 'bar':
		plot = plotly.offline.plot({
			"data": [plotly.graph_objs.Bar(x=dataX, y=dataY, marker=dict(color=lineColor))],
			"layout": Layout(title=country + " - " + dataType + " daily cases", height=800, margin=dict(
				l=50,
				r=50,
				b=100,
				t=100,
			))
		}, output_type='div'
		)
		'''
		, include_plotlyjs=False
		, output_type='div'
		'''
		return plot

	elif chartType == 'linear':
		plot = plotly.offline.plot({
			"data": [Scatter(x=dataX, y=dataY, marker=dict(color=lineColor,size=120))],
			"layout": Layout(title=country + " - Total " + dataType + " cases", height=800 ,margin=dict(
				l=50,
				r=50,
				b=100,
				t=100,
			))
		}, output_type='div'
		)
		'''
		, include_plotlyjs=False
		, output_type='div'
		'''
		return plot

	

##########################################################

# if __name__ == '__main__':
	# summary = getSummary('Japan')
	# print(summary)

	# examplePlot()