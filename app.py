import requests
import csv
from flask import Flask
from flask import render_template
from flask import redirect, request

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
print(data[0]["rates"])
rates = data[0]["rates"]

with open('plik.csv', 'w') as csvfile:
    fieldnames = ['currency','code','bid','ask']
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=";")
    csvwriter.writeheader()
    for n in rates:
        csvwriter.writerow(n)

codes = ["USD", "AUD","CAD","EUR","HUF","CHF","GBP","JPY","CZK","DKK","NOK","SEK","XDR"]

@app.route('/', methods=['GET', 'POST'])
def kantor():
   kwota=None
   if request.method == 'POST':
       amount =request.form["amount"]
       for rate in rates:
           if rate["code"] == request.form["codes"]:
            kwota = round((float(rate["ask"])*float(amount)),2)
   return render_template("form.html",rates=rates, result=kwota)        
