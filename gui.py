from flask import Flask, render_template, request, redirect, url_for, flash
from TweakersScraper import getProductpage, getPrices, getAveragePrice, getMedianPrice, getProductSpecs

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product = request.form['product']
        if product is None or product == "":
            product = "Gelieve een product in te geven"
            return render_template('index.html', product=product)
        data = getPrices(getProductpage(product))
        if data is None:
            product = "Gelieve een geldig product in te geven"
        # the html page has a table with id "tabel", fill it with the data
        specs = getProductSpecs(getProductpage(product))
        ean = specs["EAN"]
        avg = getAveragePrice(data["items"])
        med = getMedianPrice(data["items"])
        return render_template('index.html', product=data["name"], data=data["items"], avg="Gemiddelde: € "+str(avg), med="Mediaan: € "+str(med), EAN="EAN: "+ean)
        

    return render_template('index.html')

app.run(host='0.0.0.0', port=80)