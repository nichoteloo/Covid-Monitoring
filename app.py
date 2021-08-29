import os
import helper
import requests
from helper.helper_ import getCountries, getSlugCountry, getOptionCountries, getSummary, preparePlotting, buildPlot, callApi
from flask import Flask, render_template, request, send_from_directory, Markup

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
			## request directly from api and visualize in chart
			fromDayOne = callApi(helper.TOTAL_FROM_DAY_ONE_BY_COUNTRY + slug[0][0])
			shortlisted = [(fromDayOne[i]['{0}'.format(dataType)], fromDayOne[i]['Date']) for i in range(len(fromDayOne))]
			dataDictionaryDaily = preparePlotting(shortlisted)

			if (not dataDictionaryDaily["Y"]) and (not dataDictionaryDaily["X"]):
				print("No Data")
				noDataMsg = "<div class='alert alert-danger' role='alert'> Sorry, there is no data available at the moment for this country. </div>"
				dailyCasesPlotHtml = Markup(noDataMsg)
			else:
				dailyPlot = buildPlot(dataDictionaryDaily["Y"], dataDictionaryDaily["X"], country, dataType, 'linear')
				dailyCasesPlotHtml = Markup(dailyPlot)
	else:
		totalCases = "-"
		totalDeaths = "-"
		totalRecovered = "-"
		optionHTML = getOptionCountries()

	return render_template('/index.html', dailyCasesPlot=dailyCasesPlotHtml, totalCases = totalConfirmed, totalDeaths = totalDeaths, totalRecovered = totalRecovered, countriesOptions=optionHTML)