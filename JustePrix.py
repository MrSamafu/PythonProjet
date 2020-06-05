#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,render_template,request
import requests
import json
from random import randint

app = Flask(__name__)

data = {}



@app.route('/', methods=['get', 'post'])
def Home():
    if request.method == 'POST':
        print("je passe la")
        reponse = request.form["prixObjet"]
        data['tentative'] = data['tentative'] + reponse
        data['reponse'] = reponse
        if int(reponse) < data["price"]:
            data["resultat"] = "C'est plus ! Recommence !"
        elif int(reponse) > data["price"]:
            data["resultat"] = "C'est moins ! Recommence !"
        elif int(reponse) == data['price']:
            
            data["resultat"] = "Bravo c'est exatcement ça !!!"
        
    else:
        
        print("je prefere passer la")
        r = JSON()
        product = r['Products'][0]['Name']
        priceProduct = r['Products'][0]['BestOffer']['SalePrice']
        imgProduct = r['Products'][0]['MainImageUrl']
        descProduct = r['Products'][0]['Description']
        data['product']=product
        data['price']=int(float(priceProduct))
        data['image']=imgProduct
        data['description']=descProduct
        data['reponse'] = 0
        data["resultat"]="A vous de jouer, trouver le prix de cette objet !"
        data["tentative"] = '0'
    return render_template('index.html', title="Le Juste Prix", data=data)
    

def JSON():
    URL = "https://api.cdiscount.com/OpenApi/json/Search"
    ApiKey = "9db668f5-3301-4ee9-a628-31b4e2e32e01"
    productNumber = randint(1, 16)
    print(productNumber)
    params = {
              "ApiKey": ApiKey,
              "SearchRequest": {
                "Keyword": "clavier",
                "Pagination": {
                  "ItemsPerPage": 1,
                  "PageNumber": productNumber
                },
                "Filters": {
                  "Price": {
                    "Min": 0,
                    "Max": 400
                  },
                  "Navigation": "computers",
                  "IncludeMarketPlace": "false"
                }
              }
            }
    r = requests.post(URL, data=json.dumps(params, indent=4))
    product = r.json()
    return product

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)