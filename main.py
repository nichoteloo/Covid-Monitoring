import os
import urls
import requests
from helper_ import getCountries, getSlugCountry, getOptionCountries, getSummary, callApi
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
		if country != 'None' and dataType != 'None':
			optionHTML = getOptionCountries()
			slug = getSlugCountry(country)
			totalCountry = getSummary(country)

			## get last update from list
			if totalCountry[0][0] is not None:
				totalConfirmed = str(totalCountry[0][0])
			if totalCountry[0][1] is not None:
				totalDeaths = str(totalCountry[0][1])
			if totalCountry[0][2] is not None:
				totalRecovered = str(totalCountry[0][2])
			
			## try to figure a chart
			fromDayOne = callApi(urls.TOTAL_FROM_DAY_ONE_BY_COUNTRY + slug[0][0])
			shortlisted = [(fromDayOne[i]['{0}'.format(dataType)], fromDayOne[i]['Date']) for i in range(len(fromDayOne))]

	else:
		totalCases = "-"
		totalDeaths = "-"
		totalRecovered = "-"
		optionHTML = getOptionCountries()

	return render_template('/index.html', totalCases = totalConfirmed, totalDeaths = totalDeaths, totalRecovered = totalRecovered, countriesOptions=optionHTML)

if __name__ == '__main__':
	app.run(debug=True)