import requests
import csv
from flask import Flask
from flask import request, redirect
from flask import render_template

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()[0]['rates']
rates=()

with open('rates.csv', 'w', newline='') as csvfile:
    fieldnames = ['currency', 'code', 'bid', 'ask']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in data:
        writer.writerow({'currency': i['currency'], 'code': i['code'], 'bid': i['bid'], 'ask': i['ask']})




@app.route('/', methods=['GET', 'POST'])
def count():
   if request.method == 'GET':
       return render_template("1.html")
   elif request.method == 'POST':
       ask = data[request.form["currency"]]["ask"]
       value = round(ask) * int(request.form["amount"])
       print("We received POST")
       return render_template("2.html", result=value)

