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

@app.route('/zdata')
def getOneArticle():
    zipcode = request.args.get('zipcode')
    baths = request.args.get('baths')
    baths_op = request.args.get('baths_op')
    beds = request.args.get('beds')
    beds_op = request.args.get('beds_op')
    price = request.args.get('price')
    price_op = request.args.get('price_op')
    sqft = request.args.get('sqft')
    sqft_op = request.args.get('sqft_op')
    print baths_op
    print baths
    print beds_op
    print beds
    print price_op
    print price
    print sqft_op
    print sqft

    client = pymongo.MongoClient("mongodb://DJ1982:forgot@test-cluster-dj-shard-00-02-fkuxb.mongodb.net",
                                 ssl_cert_reqs=ssl.CERT_REQUIRED,
                                 ssl_ca_certs=certifi.where())
    mydb = client.projectdb
    mycol = mydb["projectData_0925"]
    x = ''

    op = {'lt': '$lt', 'gt': '$gt', 'eq': '$eq'}

    query = {"ZIP": zipcode}
    if baths != None:
        operator = op.get(baths_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'BATHS': {operator: baths}})

    if beds != None:
        operator = op.get(beds_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'BEDS': {operator: beds}})

    if price != None:
        operator = op.get(price_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'PRICE': {operator: price}})

    if sqft != None:
        operator = op.get(sqft_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'SQUARE FEET': {operator: sqft}})



    #result = [data for data in mycol.find({"ZIP": zipcode}, {"_id": 0 }).limit(5)]
    result = [data for data in mycol.find(query , {"_id": 0}).limit(15)]
    if data:
        output= "Results found"
    else:
        output="No Results Found"


    return Response(json.dumps(result),  mimetype='application/json')

@app.route('/cordinate')
def housedata():
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    baths = request.args.get('baths')
    baths_op = request.args.get('baths_op')
    beds = request.args.get('beds')
    beds_op = request.args.get('beds_op')
    price = request.args.get('price')
    price_op = request.args.get('price_op')
    sqft = request.args.get('sqft')
    sqft_op = request.args.get('sqft_op')
    print baths_op
    print baths
    print beds_op
    print beds
    print price_op
    print price
    print sqft_op
    print sqft
    pprint(longitude)
    pprint(latitude)
    client = pymongo.MongoClient("mongodb://DJ1982:forgot@test-cluster-dj-shard-00-02-fkuxb.mongodb.net",
                                 ssl_cert_reqs=ssl.CERT_REQUIRED,
                                 ssl_ca_certs=certifi.where())
    mydb = client.projectdb
    mycol = mydb["projectData_0925"]
#    mycol.create_index([('BOUNDARY', pymongo.GEOSPHERE)], name='BOUNDARY', default_language='english')
    query = {"BOUNDARY": {
        "$nearSphere": {"$geometry": {"type": "Point", "coordinates": [float(longitude), float(latitude)]},
                        "$maxDistance": 5}}}

    op = {'lt': '$lt', 'gt': '$gt', 'eq': '$eq'}
    if baths != None:
        operator = op.get(baths_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'BATHS': {operator: baths}})

    if beds != None:
        operator = op.get(beds_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'BEDS': {operator: beds}})

    if price != None:
        operator = op.get(price_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'PRICE': {operator: price}})

    if sqft != None:
        operator = op.get(sqft_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'SQUARE FEET': {operator: sqft}})

    property = mycol.find(query, {"_id": 0 }).limit(15)
    pprint(property)

    result = []
    for document in property:
       result.append(document)

    pprint(result)

    if property:
     textline = result

    else:
     textline = "no results"

    return Response(json.dumps(textline), mimetype='application/json')


@app.route('/data')
def getData():
    str = request.args.get('str') #this arg will be provided
    baths = request.args.get('baths')
    baths_op = request.args.get('baths_op')
    beds = request.args.get('beds')
    beds_op = request.args.get('beds_op')
    price = request.args.get('price')
    price_op = request.args.get('price_op')
    sqft = request.args.get('sqft')
    sqft_op = request.args.get('sqft_op')

    #rooms
    print str
    print baths_op
    print baths
    print beds_op
    print beds
    print price_op
    print price
    print sqft_op
    print sqft


    #if 'str' in request.args:
    # return 'Hello ' + request.args['str']
    #else:
    #    return 'Hello John Doe'
    client = pymongo.MongoClient("mongodb://DJ1982:forgot@test-cluster-dj-shard-00-02-fkuxb.mongodb.net",
                                 ssl_cert_reqs=ssl.CERT_REQUIRED,
                                 ssl_ca_certs=certifi.where())
    mydb = client.projectdb
    mycol = mydb["projectData_0925"]
    x = any(c.isdigit() for c in str)
    print x
    outputdata = []

    query = {}
    op = {'lt':'$lt', 'gt':'$gt', 'eq': '$eq'}
    if baths != None:
        operator = op.get(baths_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'BATHS': {operator: baths}})

    if beds != None:
        operator = op.get(beds_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'BEDS': {operator: beds}})

    if price != None:
        operator = op.get(price_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'PRICE': {operator: price}})

    if sqft != None:
        operator = op.get(sqft_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'SQUARE FEET': {operator: sqft}})

    if x == False:
        query.update({'CITY': {'$regex': str, '$options': 'i'}})
        outputdata = [data1 for data1 in mycol.find(query, {"_id": 0}).limit(15)]

    if x==True or len(outputdata) == 0:
        query['ADDRESS'] = {'$regex': str, '$options': 'i'}
        outputdata = [data1 for data1 in mycol.find(query, {"_id": 0}).limit(15)]
    #if(filter=='baths'):


    print "Selected query {}".format(query)

    #if outputdata is None :
    #    finaldata = [data1 for data1 in mycol.find({'ADDRESS': {'$regex': '.*str.*'}}, {"_id": 0}).limit(5)]

    return Response(json.dumps(outputdata),  mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


