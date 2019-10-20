# Agrifix : Detect land conditions through satellite imagery with a single click.

import json
import requests
import logging

from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request

app = Flask(__name__, static_url_path='')
usr = 'agrifix'
tkn = 'a_-_-**_-_-9'

@app.route("/", methods=['GET', 'POST'])
def root(): 
	return app.send_static_file('index.html')

@app.route('/coordinates', methods=['POST'])
def listen():
	try:
		longitude = request.form.get("longitude")
		latitude = request.form.get("latitude")	
	except Exception:
		return jsonify({"response" : "Bad request!"}), 400

	getRadasat1Images(longitude, latitude)

	return jsonify({"response" : "SUCCESS"}), 200

def getRadasat1Images(longitude, latitude):
	radarsat1_api_url = "https://data.eodms-sgdot.nrcan-rncan.gc.ca/api/dhus/v1/products/Radarsat1/search?q=footprint:Intersects((" + latitude + "," + longitude + "))"
	response = requests.get(radarsat1_api_url, auth=(usr, tkn)).content
	print(response)


if __name__ == '__main__':
	handler = RotatingFileHandler('server.log', maxBytes=10000, backupCount=1)
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	app.run(host="127.0.0.1",port=5000)

