from flask import request
from flask import Flask
import pymongo
import ssl
import certifi
import json
from pprint import pprint
from flask import Response
import os

app = Flask(__name__)


@app.route('/')
def home():
    return "Real Estate Data"

@app.route('/<zipcode>')
def getOneArticle(zipcode):
    client = pymongo.MongoClient("mongodb://DJ1982:forgot@test-cluster-dj-shard-00-02-fkuxb.mongodb.net",
                                 ssl_cert_reqs=ssl.CERT_REQUIRED,
                                 ssl_ca_certs=certifi.where())
    mydb = client.projectdb
    mycol = mydb["projectData_0925"]
    x = ''
    result = [data for data in mycol.find({"ZIP":zipcode}, {"_id": 0 }).limit(5)]
    #[doc for doc in db.units.find()]�
    #for y in data:
     #   x += y



    if data:
        output= "Results found"
    else:
        output="No Results Found"


    return Response(json.dumps(result),  mimetype='application/json')

@app.route('/cordinate')
def housedata():
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    pprint(longitude)
    pprint(latitude)
    client = pymongo.MongoClient("mongodb://DJ1982:forgot@test-cluster-dj-shard-00-02-fkuxb.mongodb.net",
                                 ssl_cert_reqs=ssl.CERT_REQUIRED,
                                 ssl_ca_certs=certifi.where())
    mydb = client.projectdb
    mycol = mydb["projectData_0925"]
    mycol.create_index([('BOUNDARY', pymongo.GEOSPHERE)], name='BOUNDARY', default_language='english')

    property = mycol.find({"BOUNDARY": {
        "$nearSphere": {"$geometry": {"type": "Point", "coordinates": [float(longitude), float(latitude)]},
                        "$maxDistance": 5}}}, {"_id": 0 }).limit(5)
    pprint(property)

    #[property for property in mycol.find({"Location" : {
    #"$nearSphere": {"$geometry": {"type": "Point", "coordinates":[-122.0160478, 37.554214]}, "$maxDistance": 500}}})
    #.limit(5)[:]]

    result = []
    for document in property:
        result.append(document)

    pprint(result)
#    textline = dumps(property)
#    pprint(textline)
    if property:
       textline=result

    else:
       textline= "no results"

    return Response(json.dumps(textline),  mimetype='application/json')
 #jsonify(textline)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


