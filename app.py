from flask import Flask, render_template, request, redirect
import requests
import json
from matplotlib import pyplot as plt
import datetime
import matplotlib.dates as mdates
import io
import base64

app = Flask(__name__,static_folder='static')
app.vars={}

def price(x):
  return '$%1.2f' % x

def plot_graph(x,y):
  years = mdates.YearLocator()   # every year
  months = mdates.MonthLocator()  # every month
  yearsFmt = mdates.DateFormatter('%Y')

  fig, ax = plt.subplots()
  ax.plot(x, y, '-')
  # format the ticks
  ax.xaxis.set_major_locator(years)
  ax.xaxis.set_major_formatter(yearsFmt)
  ax.xaxis.set_minor_locator(months)

  datemin = datetime.date(x[-1].year, 1, 1)
  datemax = datetime.date(x[0].year + 1, 1, 1)
  ax.set_xlim(datemin, datemax)

  # format the coords message box
  ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
  #ax.format_ydata = price
  ax.grid(True)

  ax.set_xlabel('Year')
  ax.set_ylabel('Price')

  # rotates and right aligns the x labels, and moves the bottom of the
  # axes up to make room for them
  fig.autofmt_xdate()

  #fig.savefig(f,format='png')
  img = io.BytesIO()
  plt.savefig(img)
  img.seek(0)
  buffer = b''.join(img)
  b2 = base64.b64encode(buffer)
  img2=b2.decode('utf-8')
  return img2


@app.route('/',methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  else:
    app.vars['symbol'] = request.form['symbol']
    app.vars['type'] = request.form['type']
    url="https://www.quandl.com/api/v3/datasets/WIKI/"+app.vars['symbol']+"/data.json?api_key=byQfxaddsZhrN9xjm_e1"
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
    img = plot_graph(x,y)
    return render_template('results.html',symbol=app.vars['symbol'], typ=app.vars['type'],stock=img)
  #return 'request.method was not a GET!'

@app.route('/results_page/<stock>')
def results(stock):
  #return "<img src= {{ url_for('static',filename='graph.png') }} >" 
  return render_template('results.html', title=stock)

'''
@app.route('/fig/<stock>')
def fig(stock):
  url="https://www.quandl.com/api/v3/datasets/WIKI/"+app.vars['symbol']+"/data.json?api_key=byQfxaddsZhrN9xjm_e1"
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
  img = plot_graph(x,y)
  return send_file(img, mimetype='image/png')
'''

if __name__ == '__main__':
  app.run(port=33507,debug=True)
