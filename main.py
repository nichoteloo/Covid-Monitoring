import os
import urls
import requests
from helper_ import getCountries, getSlugCountry, getOptionCountries, callApi
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
	totalCases = "-"
	totalDeaths = "-"
	totalRecovered = "-"
	
	optionHTML = getOptionCountries()

	return render_template('/index.html', totalCases=totalCases, totalDeaths=totalDeaths, totalRecovered=totalRecovered, countriesOptions=optionHTML)

@app.route('/chart', methods=['GET'])
def chart():
	if request.method == 'GET':
		country = request.args.get('country')
		dataType = request.args.get('dataType')
		if bool(country) & bool(dataType):
			temp = []
			optionHTML = getOptionCountries()
			slug = getSlugCountry(country)

			totalCountry = callApi(urls.TOTAL_FROM_DAY_ONE_BY_COUNTRY + slug[0][0])

			for i in range(len(totalCountry)):
				if totalCountry[i]['Country'] == country:
					temp.append(totalCountry[i])
					break
				else:
					temp = []

			if temp[0]['Confirmed'] is not None:
				print(temp[0]['Confirmed'])
				totalConfirmed = str(temp[0]['Confirmed'])
			if temp[0]['Deaths'] is not None:
				print(temp[0]['Deaths'])
				totalDeaths = str(temp[0]['Deaths'])
			if temp[0]['Recovered'] is not None:
				print(temp[0]['Recovered'])
				totalRecovered = str(temp[0]['Recovered'])

	return render_template('/index.html', totalCases = totalConfirmed, totalDeaths = totalDeaths, totalRecovered = totalRecovered, countriesOptions=optionHTML)

if __name__ == '__main__':
	app.run(debug=True)