# Agrifix : Detect land conditions through satellite imagery with a single click.

import json
import requests
import logging

from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request

app = Flask(__name__, static_url_path='')

@app.route("/", methods=['GET', 'POST'])
def root(): 
	return app.send_static_file('index.html')

@app.route('/coordinates', methods=['GET', 'POST'])
def listen():
	try:
		query = json.loads(request.data)
		longitude = query['longitude'].lower()
		latitude = query['latitude'].lower()		
	except Exception:
		return jsonify({"response" : "Bad request!"}), 400

	return jsonify({"response" : "SUCCESS"}), 200 

if __name__ == '__main__':
	handler = RotatingFileHandler('server.log', maxBytes=10000, backupCount=1)
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	app.run(host="127.0.0.1",port=5000)

