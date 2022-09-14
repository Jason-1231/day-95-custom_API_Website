import requests
import json
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

API_KEY = "defb567ab6ff6f02e81e0700d4208115"
BASE_URL = "http://api.marketstack.com/v1/eod"
WATCH_LIST = ['TSLA', 'AAPL', 'DSY.XJSE']

app = Flask(__name__)
Bootstrap(app)


@app.route("/")
def home():
    dates = []
    closes = []
    symbols = []

    for stock in WATCH_LIST:
        params = {
            "access_key": API_KEY,
            "symbols": stock
        }
        response = requests.get(BASE_URL, params=params)
        print(response)

        with open(f'{stock}.json', 'w') as write_file:
            json.dump(response.json(), write_file, indent=4)

        with open(f'{stock}.json') as file:
            data = json.load(file)
        dates.append(data['data'][0]['date'].split('T')[0])
        closes.append(data['data'][0]['close'])
        symbols.append(data['data'][0]['symbol'])

    return render_template("index.html",
                           dates=dates,
                           closes=closes,
                           symbols=symbols,
                           watch_list=WATCH_LIST)


@app.route("/<symbol>")
def stock_page(symbol):
    with open(f'{symbol}.json') as f:
        data = json.load(f)
    latest_date = data['data'][0]['date'].split('T')[0]
    latest_open = data['data'][0]['open']
    latest_close = data['data'][0]['close']
    percentage_change = round((latest_close - latest_open) / latest_open * 100, 2)
    return render_template('stock.html',
                           symbol=symbol,
                           date=latest_date,
                           open=latest_open,
                           close=latest_close,
                           change=percentage_change)


if __name__ == '__main__':
    app.run(debug=True)