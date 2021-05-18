## https://github.com/albino98/Covid19Monitoring/blob/9b10d3f9aa7894c77e7f966d184657c097ab5627/covid19Monitoring/main.py#L221

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
	return "helloo flask"

@app.route('/country')
def getCountry():



if __name__ == '__main__':
	app.run(debug=True)