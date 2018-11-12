import pandas as pd
# import numpy as np
import os
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split


class PredictPriceKNNModel:
    modified_file_path = ""

    def __init__(self):
        # Using constructor to initialize global variable, else it will give error in function
        global modified_file_path
        modified_file_path = os.path.join(os.getcwd(), "udata_modified.csv")

    def get_pd_for_predict_price(self, zip_code, beds, baths, square_feet, lot_size, year_build):
        dict_predict_property = {
            'ZIP_NEW': [zip_code],
            'BEDS': [beds],
            'BATHS': [baths],
            'SQUARE_FEET': [square_feet],
            'LOT SIZE': [lot_size],
            'YEAR_BUILT': [year_build]
        }

        pd_predict_property = pd.DataFrame.from_dict(dict_predict_property)
        return pd_predict_property

    def get_price_prediction(self, zip_code, beds, baths, square_feet, lot_size, year_build):
        predict_property_price = self.get_pd_for_predict_price(zip_code, beds, baths, square_feet, lot_size, year_build)
        # global file_name
        file_name = 'udata_0925.csv'
        model_file_path = os.path.join(os.getcwd(), file_name)

        print "Path to access csv file to train model" + model_file_path

        data = pd.read_csv(model_file_path, sep=',', encoding='utf-8', usecols=
                            [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 23, 24, 25, 26])

        # Removing outliers and filtering records for a State
        price_frame = data.loc[(data['PRICE'] > 80000) & (data['PRICE'] < 26000000)].copy()
        price_frame = price_frame.loc[(price_frame['DAYS ON MARKET'] < 700)].copy()
        price_frame = price_frame.loc[price_frame['STATE'] == 'CA'].copy()
        print "Number  of records to be used to train model" + str(price_frame.shape)

        data = pd.DataFrame(data=price_frame, columns=['ZIP_NEW', 'BEDS', 'BATHS', 'SQUARE_FEET', 'LOT SIZE',
                                                       'YEAR_BUILT', 'PRICE'])
        # ,'Livability'
        target = pd.DataFrame(data=price_frame, columns=['PRICE'])

        data['BEDS'].fillna(2, inplace=True)
        data['BATHS'].fillna(0, inplace=True)
        data['YEAR_BUILT'].fillna(1980, inplace=True)
        data['LOT SIZE'].fillna(data['BATHS']*700, inplace=True)
        data['SQUARE_FEET'].fillna(data['BEDS']*700, inplace=True)
        data['ZIP_NEW'].fillna(94041, inplace=True)

        #modified_file_path = os.path.join(os.environ['HOME'], "udata_modified.csv")
        global modified_file_path
        # modified_file_path = os.path.join(os.getcwd(), "udata_modified.csv")
        print("Modified csv file path {0}".format(modified_file_path))
        data.to_csv(modified_file_path)
        # To get statistic of the data and target frame
        self.get_pd_data_statistic(data, target)

        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.0)
        print X_train.shape, y_train.shape
        print X_test.shape, y_test.shape
        # Create the knn model.
        # Look at the 20 closest neighbors.
        knn = KNeighborsRegressor(n_neighbors=20)
        # Fit the model on the training data.
        # knn.fit(train[x_columns], train[y_column])

        knn.fit(X_train, y_train)
        # Make point predictions on the test set using the fit model.

        predictions = knn.predict(predict_property_price)

        return predictions

    def get_pd_data_statistic(self, data_pd_frame, target_pd_frame):

        data_frame = data_pd_frame[data_pd_frame.notnull().any(axis=1)]
        print "The number of records that have null values" + str(data_frame.shape)

        target_pd_frame = target_pd_frame[(target_pd_frame > 0).all(axis=1)]
        target_pd_frame = target_pd_frame[target_pd_frame.isnull().any(axis=1)]
        print "The number of target records that are null" + str(target_pd_frame.shape)

    def customized_train_model(self, zip_code, beds, baths, square_feet, lot_size, year_build):
        # Read doesn't require global keyword to refer class variable
        print("Customized train model path {0}".format(modified_file_path))
        data = pd.read_csv(modified_file_path, sep=',', encoding='utf-8')

        target = pd.DataFrame(data=data, columns=['PRICE'])
        data = pd.DataFrame(data=data, columns=['ZIP_NEW', 'BEDS', 'BATHS', 'SQUARE_FEET', 'LOT SIZE', 'YEAR_BUILT'])
        # ,'Livability'

        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.0)
        print X_train.shape, y_train.shape
        print X_test.shape, y_test.shape
        # Create the knn model.
        # Look at the 20 closest neighbors.
        knn = KNeighborsRegressor(n_neighbors=20)
        # Fit the model on the training data.
        knn.fit(X_train, y_train)
        # Make point predictions on the test set using the fit model.
        predict_property_price = self.get_pd_for_predict_price(zip_code, beds, baths, square_feet, lot_size, year_build)
        predictions = knn.predict(predict_property_price)

        return predictions


if __name__ == '__main__':
    model = PredictPriceKNNModel()
    # predicted_price = model.get_price_prediction(zip_code=94041, beds=4, baths=2, square_feet=1800, lot_size=3000, year_build=1985)
    # print "The predicted price for parameterized property is" + str(predicted_price)
    predicted_price = model.customized_train_model(zip_code=94041, beds=4, baths=2, square_feet=1800, lot_size=3000, year_build=1985)
    print "The predicted price for parameterized property is" + str(predicted_price)
    print type(str(predicted_price))