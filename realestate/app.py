from flask import request
from flask import Flask
import pymongo
import ssl
import certifi
import json
from pprint import pprint
from flask import Response
import os
# from predict_price_knn_model import PredictPriceKNNModel
from flask import send_file

from ImagesHelper import ImageHelper
import io

app = Flask(__name__)

img_helper = ImageHelper()

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
    sortv = request.args.get('sortv')
    sort_by= request.args.get('sort_by')
    skip_rec = request.args.get('skip')

    client = pymongo.MongoClient("mongodb://du1982:forgot@realestate-shard-00-01-pazv8.mongodb.net",
                                 ssl_cert_reqs=ssl.CERT_REQUIRED,
                                 ssl_ca_certs=certifi.where())
    mydb = client.realestate
    mycol = mydb["realEstateData"]
    x = ''
    data = ''
    op = {'lt': '$lt', 'gt': '$gt', 'eq': '$eq'}

    query = {"ZIP": zipcode}
    if baths != None:
        operator = op.get(baths_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'BATHS': {operator: float(baths)}})

    if beds != None:
        operator = op.get(beds_op);
        print operator
        print "selected operator {}".format('$' + "operator")
        query.update({'BEDS': {operator: int (beds)}})

    if price != None:
        operator = op.get(price_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'PRICE': {operator: float (price)}})

    if sqft != None:
        operator = op.get(sqft_op);
        print "selected operator {}".format('$' + "operator")
        query.update({'SQUARE FEET': {operator: float(sqft)}})

    no_of_rec_to_skip = int(skip_rec)
    if sortv!= None:
        if sortv == 'price':
            result = [data for data in mycol.find(query, {"_id": 0}).sort([("PRICE", int(sort_by))]).skip(no_of_rec_to_skip).limit(15)]
        elif sortv == 'beds':
            result = [data for data in mycol.find(query, {"_id": 0}).sort([("BEDS", int(sort_by))]).skip(no_of_rec_to_skip).limit(15)]
        elif sortv == 'baths':
            result = [data for data in mycol.find(query, {"_id": 0}).sort([("BATHS", int(sort_by))]).skip(no_of_rec_to_skip).limit(15)]
        elif sortv == 'sqft':
            result = [data for data in mycol.find(query, {"_id": 0}).sort([("SQUARE FEET", int(sort_by))]).skip(no_of_rec_to_skip).limit(15)]
    else:
        result = [data for data in mycol.find(query, {"_id": 0}).skip(no_of_rec_to_skip).limit(15)]

    result = img_helper.get_images_for_property(result)

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
    client = pymongo.MongoClient("mongodb://du1982:forgot@realestate-shard-00-01-pazv8.mongodb.net",
                                 ssl_cert_reqs=ssl.CERT_REQUIRED,
                                 ssl_ca_certs=certifi.where())

    mydb = client.realestate
    mycol = mydb["realEstateData"]
    #mycol.create_index([('BOUNDARY', pymongo.GEOSPHERE)], name='BOUNDARY', default_language='english')
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

    # img_helper.get_images_for_property(result)

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
    skip_rec = request.args.get('skip')

    no_of_rec_to_skip = int(skip_rec)
    client = pymongo.MongoClient("mongodb://du1982:forgot@realestate-shard-00-01-pazv8.mongodb.net",
                                 ssl_cert_reqs=ssl.CERT_REQUIRED,
                                 ssl_ca_certs=certifi.where())
    mydb = client.realestate
    mycol = mydb["realEstateData"]
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
        outputdata = [data1 for data1 in mycol.find(query, {"_id": 0}).skip(no_of_rec_to_skip).limit(15)]

    if x==True or len(outputdata) == 0:
        query['ADDRESS'] = {'$regex': str, '$options': 'i'}
        outputdata = [data1 for data1 in mycol.find(query, {"_id": 0}).skip(no_of_rec_to_skip).limit(15)]
    #if(filter=='baths'):

    print "Selected query {}".format(query)

    #if outputdata is None :
    #    finaldata = [data1 for data1 in mycol.find({'ADDRESS': {'$ regex': '.*str.*'}}, {"_id": 0}).limit(5)]

    img_helper.get_images_for_property(outputdata)
    return Response(json.dumps(outputdata),  mimetype='application/json')

@app.route('/getImage')
def getImage():
    # image_path = os.path.join(os.getcwd(), "../images/Condo/house1/1.jpg")
    image_path = "./images/Condo/house1/1.jpg"
    print ("Image path -- {0}".format(image_path))
    return send_file(image_path, mimetype='image/jpg')

#
# @app.route('/price_prediction')
# def getPricePrediction():
#     zip_code = request.args.get('zip_code')
#     beds = request.args.get('beds')
#     baths= request.args.get('baths')
#     square_feet = request.args.get('square_feet')
#     lot_size = request.args.get('lot_size')
#     year_build = request.args.get('year_build')
#
#     model = PredictPriceKNNModel()
#     predicted_price = model.customized_train_model(zip_code=zip_code, beds=beds, baths=baths, square_feet=square_feet,
#                                                    lot_size=lot_size,year_build=year_build)
#     print "The predicted price for parameterized property is" + str(predicted_price)
#     return Response(str(predicted_price), mimetype='text')

@app.route('/property_image')
def get_property_image():
    image_url = request.args.get('image_url')
    return send_file(image_url, mimetype='image/jpg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

