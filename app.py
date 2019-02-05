from flask import Flask, render_template, request, redirect
import requests
import quandl
import json
from matplotlib import pyplot as plt
import datetime
import io
#import base64
from bokeh.embed import components,file_html
from bokeh.resources import CDN
from bokeh.plotting import figure

app = Flask(__name__,static_folder='static')
app.vars={}

def dateFormat(aDatetime):
	return ("%s-%s-%s" % (aDatetime.year, aDatetime.month, aDatetime.day))

@app.route('/',methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		app.vars['symbol'] = request.form['symbol']
		app.vars['type'] = request.form['type']
		print(app.vars['symbol'],app.vars['type'])
		url="https://www.quandl.com/api/v3/datasets/WIKI/"+app.vars['symbol']+"/data.json?api_key=byQfxaddsZhrN9xjm_e1"
		#now = datetime.datetime.now()
		#stockDF = quandl.get("WIKI/"+app.vars['symbol'],returns='pandas',\
		#				   	end_date=dateFormat(now), start_date=dateFormat(now-datetime.timedelta(days=30)))
		#print(stockDF.head())
		response = requests.get(url)
		data = json.loads(response.text)
		raw = data['dataset_data']['data']
		x = []
		y = []
		for a in raw:
			x.append(datetime.datetime.strptime(a[0],'%Y-%m-%d'))
			if app.vars['type'] == 'Open Price':
				y.append(float(a[1]))
			elif app.vars['type'] == 'Close Price':
				y.append(float(a[4]))
			elif app.vars['type'] == 'Adjusted Open Price':
				y.append(float(a[8]))
			elif app.vars['type'] == 'Adjusted Close Price':
				y.append(float(a[11]))
		plot = figure(tools="", title='Data from Quandle WIKI set', x_axis_label='Date', x_axis_type='datetime',\
					y_axis_label=app.vars['type']+" Price")
		'''
		if app.vars['type'] == 'Open Price':
			plot.line(stockDF.index.values.tolist(), stockDF['Open'].values.tolist())
		elif app.vars['type'] == 'Close Price':
			plot.line(stockDF.index.values.tolist(), stockDF['Close'].values.tolist())
		elif app.vars['type'] == 'Adjusted Open Price':
			plot.line(stockDF.index.values.tolist(), stockDF['Adjusted Open'].values.tolist())
		elif app.vars['type'] == 'Adjusted Close Price':
			plot.line(stockDF.index.values.tolist(), stockDF['Adjusted Close'].values.tolist())
		'''
		plot.line(x,y)
		#print('Plot made.')
		return file_html(plot, CDN, "myplot")


if __name__ == '__main__':
	app.run(port=33507,debug=True)
