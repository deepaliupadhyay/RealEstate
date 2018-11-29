import pandas as pd
import numpy as np
import os
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
import sys
from sklearn.metrics import r2_score
from sklearn.svm import SVR
import sklearn.svm
# import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt

from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import QuantileTransformer, quantile_transform



class PredictPriceKNNModel:
    modified_file_path = ""

    def __init__(self):
        # Using constructor to initialize global variable, else it will give error in function
        global modified_file_path
        modified_file_path = os.path.join(os.getcwd(), "udata_modified.csv")



    def read_data(self):
        file_name = os.path.join(os.getcwd(), "price_prediction_data_v1.csv")

        print("Path to access csv file to train model" + file_name)

        data = pd.read_csv(file_name, sep=',', encoding='utf-8')
        print(data.columns)
        data = pd.DataFrame(data=data, columns=[
            #'SALE TYPE',
             'property_type', #'STATE',
            'zip', 'PRICE', 'beds', 'baths',
            'sq_ft',  # 'lot_size',
            'year_built', 'days_on_market',
            'price_per_sq_ft',
            #'cost_of_living', 'Housing', 'Crime',
            #'State', 'Weather', 'Amenities', 'Education', 'Employment',
            'Livability'])

        print("Total records in dataset - {0}".format(data.shape))
        # Find Missing Ratio of Dataset
        all_data_na = (data.isnull().sum() / len(data)) * 100
        all_data_na = all_data_na.drop(all_data_na[all_data_na == 0].index).sort_values(ascending=False)[:30]
        missing_data = pd.DataFrame({'Missing Ratio': all_data_na})
        print(missing_data)

        data = data.loc[data['STATE'] == 'CA'].copy()
        data = data.loc[(data['zip'] > 90500) & (data['zip'] < 96000)].copy()
        data = data.loc[(data['beds'] < 7)].copy()
        data = data.loc[(data['baths'] >= 1) & (data['baths'] <= 6)].copy()
        data = data.loc[(data['year_built'] > 1950)].copy()
        data = data.loc[(data['PRICE'] > 80000) & (data['PRICE'] < 4000000)].copy()
        data = data.loc[
            (data['property_type'] == 'Single Family Residential') | (data['property_type'] == 'Townhouse') | (
                        data['property_type'] == 'Condo/Co-op')].copy()
        data = data.loc[(data['sq_ft'] < 4400)].copy()

        print("Records after Winsoring - {0}".format(data.shape))
        all_data_na = (data.isnull().sum() / len(data)) * 100
        all_data_na = all_data_na.drop(all_data_na[all_data_na == 0].index).sort_values(ascending=False)[:30]
        missing_data = pd.DataFrame({'Missing Ratio': all_data_na})
        print(missing_data)

        data = data.dropna()
        print("Records after NAN deletion - {0}".format(data.shape))

        # One-hot encoding
        data = pd.concat([data, pd.get_dummies(data['property_type'], prefix='property_type')], axis=1)
        # now drop the original 'country' column (you don't need it anymore)
        data.drop(['property_type'], axis=1, inplace=True)

        # One-hot encoding
        data = pd.concat([data, pd.get_dummies(data['cost_of_living'], prefix='cost_of_living')], axis=1)
        # now drop the original 'country' column (you don't need it anymore)
        data.drop(['cost_of_living'], axis=1, inplace=True)

        # One-hot encoding
        data = pd.concat([data, pd.get_dummies(data['Weather'], prefix='Weather')], axis=1)
        # now drop the original 'country' column (you don't need it anymore)
        data.drop(['Weather'], axis=1, inplace=True)

        return data


    def customized_train_model(self, zip_code, beds, baths, square_feet, year_build, price_per_sq_ft):
        data = self.read_data()

        print("Finally total number of records to be used for train model" + str(data.shape))

        target = pd.DataFrame(data=data, columns=['PRICE'])
        data = pd.DataFrame(data=data, columns=[
            'property_type_Condo/Co-op',
            'property_type_Single Family Residential',
            'property_type_Townhouse',
            'zip',
            'beds',
            'baths',
            'sq_ft',
            'year_built',
            'Livability'#,
            #'price_per_sq_ft'
        ])

        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.3, random_state=8456)
        print("Shape of X_train {0}", X_train.shape)
        print("Shape of X_test {0}", X_test.shape)
        print("Shape of y_train {0}", y_train.shape)
        print("Shape of y_test {0}", y_test.shape)




        regression = RandomForestRegressor(bootstrap=True, criterion='mse', max_depth=5,
                                           max_leaf_nodes=None, min_impurity_decrease=0.0,
                                           min_impurity_split=None, min_samples_leaf=3,
                                           min_samples_split=8, min_weight_fraction_leaf=0.0,
                                           n_estimators=5, n_jobs=-1, oob_score=False, random_state=None,
                                           verbose=0, warm_start=False)
        regression.fit(X_train, y_train.values.ravel())
        predict_property_price = self.get_pd_for_predict_price(zip_code, beds, baths, square_feet , year_build, price_per_sq_ft)
        predictions=regression.predict(predict_property_price)
        return predictions

    def get_pd_for_predict_price(self, zip_code, beds, baths, square_feet, year_build, price_per_sq_ft):
        dict_predict_property = {
            'property_type_Condo/Co-op':[1],
            'property_type_Single Family Residential':[0],
            'property_type_Townhouse': [0],
            'zip': [zip_code],
            'beds': [beds],
            'baths': [baths],
            'sq_ft': [square_feet],
            'year_built': [year_build],
            'Livability': [74]#,
            #'price_per_sq_ft': [str(price_per_sq_ft)]

            # {
            #     "BEDS": 1,
            #     "YEAR BUILT": "1984",
            #     "BATHS": 1.0,
            #     "ZIP": "94539",
            #     "COST_SQUARE_FEET": "750",
            #     "SQUARE FEET": 665.0,
            #     "PRICE": 499000.0,
            #     "PROPERTY TYPE": "Condo/Co-op"
            # }
        }

        pd_predict_property = pd.DataFrame.from_dict(dict_predict_property)
        return pd_predict_property


if __name__ == '__main__':
    model = PredictPriceKNNModel()
    predicted_price = model.customized_train_model(zip_code=94539, beds=1, baths=1, square_feet=665, year_build=1984, price_per_sq_ft="750" )
    print "The predicted price for parameterized property is" + str(predicted_price)
    print type(str(predicted_price))