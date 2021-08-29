import helper
from helper.helper_ import callApi, MySQLConnect

## Inject Country for Once	
def allCountry():
	totalCountry = callApi(helper.COUNTRIES)
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
	summary = callApi(helper.SUMMARY)
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