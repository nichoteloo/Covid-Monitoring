import os
import pdb
import json
import yaml
import urllib.request
from flask import Flask, Markup, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

BASE_URL = "https://api.covid19api.com/"
SUMMARY = "summary"
TOTAL_FROM_DAY_ONE_BY_COUNTRY = "total/dayone/country/"

# configure db
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

# instanciate
mysql = MySQL(app)

def getCountry():
	cur = mysql.connection.cursor()
	cur.execute("SELECT Country FROM countries")
	countries = cur.fetchall()
	cur.close()

	option = ""
	for country in countries:
		option = option + "<option value='" + str(country[0]).lstrip().replace(" ","-") + "'>" + str(country[0]).lstrip() + "</option>\n"
	htmlOptions = Markup(option)
	return htmlOptions

def callApi(route):
	with urllib.request.urlopen(BASE_URL + route) as url:
		data = json.loads(url.read().decode())
		return data

@app.route('/')
def index():
	optionHtml = getCountry()
	totalCases="-"
	totalDeaths="-"
	totalRecovered="-"
	return render_template('/index.html', totalCases=totalCases, totalDeaths=totalDeaths, countriesOptions=optionHtml, totalRecovered=totalRecovered)

@app.route('/chart', methods=['GET'])
def chart():
	if request.method == 'GET':
		country = request.args.get('country')
		dataType = request.args.get('dataType')

		totalCountry = callApi(TOTAL_FROM_DAY_ONE_BY_COUNTRY + country)
		pdb.set_trace()
		return render_template('/index.html')

if __name__ == '__main__':
	app.run(debug=True)