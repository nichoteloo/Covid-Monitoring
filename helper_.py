import urls
import yaml
import requests
import mysql.connector
from flask import Markup

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
	response = requests.get(urls.BASE_URL + route).json()
	return response

## Inject Country for Once	
def allCountry():
	totalCountry = callApi(urls.COUNTRIES)
	mydb = MySQLConnect()
	for x in totalCountry:
		country = x["Country"]
		slug = x["Slug"]
		iso2 = x["ISO2"]

		cur = mydb.cursor()
		cur.execute("INSERT INTO `countries` (`Country`, `Slug`, `ISO2`) VALUES (%s,%s,%s);", (country , slug, iso2))
		mydb.commit()
		print(cur.rowcount, "record affected.")
	cur.close()

## Inject Country for Once
def countrySummary():
	summary = callApi(urls.SUMMARY)
	mydb = MySQLConnect()
	for country in summary['Countries']:
		id_ = country["ID"]
		country_ = country["Country"]
		country_code = country["CountryCode"]
		slug = country["Slug"]
		new_confirmed = country["NewConfirmed"]
		total_confirmed = country["TotalConfirmed"]
		new_deaths = country["NewDeaths"]
		total_deaths = country["TotalDeaths"]
		new_recovered = country["NewRecovered"]
		total_recovered = country["TotalRecovered"]
		date = country["Date"].split("T")[0]

		cur = mydb.cursor()
		sql = "INSERT INTO `dailysummary`(`ID`, `Country`, `CoutryCode`, `Slug`, `NewConfirmed`, `TotalConfirmed`, `NewDeaths`, `TotalDeaths`, `NewRecovered`, `TotalRecovered`, `Date`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		val = (id_,country_,country_code,slug,new_confirmed,total_confirmed,new_deaths,total_deaths,new_recovered,total_recovered,date)
		cur.execute(sql, val)
		mydb.commit()
		print(cur.rowcount, "record affected.")
	mydb.close()

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

## Save Current 

##########################################################

# if __name__ == '__main__':
	# allCountry()
	# countrySummary()