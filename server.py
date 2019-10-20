# Agrifix : Detect land conditions through satellite imagery with a single click.

import json
import requests
import logging
import reverse_geocoder
import requests
from requests.auth import HTTPBasicAuth
import glob, os

from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request

app = Flask(__name__, static_url_path='')
usr = 'agrifix'
tkn = 'a_-_-**_-_-9'

@app.route("/", methods=['GET', 'POST'])
def root():
	return app.send_static_file('index.html')

@app.route('/reverse_geocode', methods=['POST'])
def get_reverse_geocode():
	try:
		longitude = request.form.get("longitude")
		latitude = request.form.get("latitude")	
	except Exception:
		return jsonify({"response" : "Bad request!"}), 400

	return json.dumps(reverse_geocoder.search((longitude, latitude))), 200

@app.route('/coordinates', methods=['POST'])
def get_images():
	try:
		longitude = request.form.get("longitude")
		latitude = request.form.get("latitude")
	except Exception:
		return jsonify({"response" : "Bad request!"}), 400

	return getRadasat1Images(longitude, latitude), 200

def getRadasat1Images(longitude, latitude):
	radarsat1_api_url = "https://data.eodms-sgdot.nrcan-rncan.gc.ca/api/dhus/v1/products/Radarsat1/search?q=footprint:Intersects((" + latitude + "," + longitude + "))"
	response = requests.get(radarsat1_api_url, auth=(usr, tkn)).json()
	localdir=os.path.dirname(os.path.abspath(__file__))
	test = localdir+"/static/images/radarsat1/original/*"
	r = glob.glob(test)
	for i in r:
   		os.remove(i)

	response_array = []
	for entry in range(len(response['entry'])):
		image_date = response["entry"][entry]['beginposition']
		linklist=response["entry"][entry]['link']
		for el in range(len(linklist)):
			if linklist[el].get('rel')=='alternative':
				img=requests.get(linklist[el].get('href'), auth=HTTPBasicAuth("Saif Kurdi-Teylouni", "Workfreedom1!"), verify=False)
				title=img.url.split("FeatureID=")[1].split("&")[0]+".png"
				image_pair = {"date" : image_date, "image_url" : title}
				if img.status_code == 200:
				    with open(localdir+"/static/images/radarsat1/original/"+title, 'wb') as f:
				        f.write(img.content)
		response_array.append(image_pair)

	# Sort the images by date.
	response_array.sort(key = lambda x:x['date'])

	return json.dumps(response_array)

if __name__ == '__main__':
	handler = RotatingFileHandler('server.log', maxBytes=10000, backupCount=1)
	handler.setLevel(logging.INFO)
	app.logger.addHandler(handler)
	app.run(host="127.0.0.1",port=5000)
