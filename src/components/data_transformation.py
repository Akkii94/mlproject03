## Importing all library

import sys
from dataclasses import dataclass
import pandas as pd
import numpy as np
import os
from src.exception import CustomException
from src.logger import logging

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocesssor.pkl')



class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
    

    def get_data_transformer_obj(self):
        '''this method is responsible for data transformation'''
        try:
            logging.info('data transformation started')

            numerical_feature = ['carat', 'depth','table', 'x', 'y', 'z']
            categorical_feature = ['cut', 'color','clarity']

            # Define the custom ranking for each ordinal variable
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']


            num_pipeline = Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())
                ]
            )
            logging.info('Numerical pipeline created')

            cat_pipeline = Pipeline(
                steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('Encoder', OneHotEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                ('scaler', StandardScaler(with_mean=False))
                ]
            )
            logging.info('categorical pipeline created')

            logging.info('categorical columns:{}'.format(categorical_feature))
            logging.info('numericals columns:{}'.format(numerical_feature))

            preprocessor = ColumnTransformer(
                [
                ('num_pipeline', num_pipeline, numerical_feature),
                ('cat_pipeline', cat_pipeline, categorical_feature)
                ]
            )

            return preprocessor
                   

        except Exception as e:
            raise CustomException(e,sys)
        
    

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Reading the train and test data')

            preprocessor_obj = self.get_data_transformer_obj()

            target_column_name = 'price'
            drop_column_name = [target_column_name, 'id']

            input_feature_train_df = train_df.drop(columns=drop_column_name, axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=drop_column_name, axis=1)
            target_feature_test_df = test_df.drop(columns=target_column_name)

            logging.info('Applying preprocessing object on training data and testing data')

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.fit_transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]


            logging.info('preprocessing done')

            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )

            logging.info('saved preprocessing object')

            return(
                train_arr,
                test_arr
            )


        except Exception as e:
            raise CustomException(e, sys)
        