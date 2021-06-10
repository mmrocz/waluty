import requests
import csv
from flask import Flask
from flask import request, redirect
from flask import render_template



response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()[0]['rates']


with open('rates.csv', 'w', newline='') as csvfile:
    fieldnames = ['currency', 'code', 'bid', 'ask']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in data:
        writer.writerow({'currency': i['currency'], 'code': i['code'], 'bid': i['bid'], 'ask': i['ask']})

app = Flask(__name__)

def currency_codes():
    codes = [code['code'] for code in data]
    return codes

@app.route("/", methods=["GET", "POST"])
def calc():
    if request.method == "POST":
        values = request.form
        currency = values.get('currency')
        amount = int(values.get('amount'))
        for i in data:
            if currency == i['code']:
                ask = round(amount * i['ask'], 1)
        return f"Koszt wymiany {amount} {currency} na PLN to {str(ask)} PLN."

    return render_template("1.html", codes=currency_codes())


if __name__ == "__main__":
    app.run(debug=True)
