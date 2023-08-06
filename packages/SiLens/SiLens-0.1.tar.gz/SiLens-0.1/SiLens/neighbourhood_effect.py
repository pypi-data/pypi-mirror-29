
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
from scipy import stats


# In[4]:

def variable_impact_in_neighbourhood(train_data, data_row, columns, predict_fn, categorical_names_encoder,
                                     encode_fn, categorical_names, categorical_features=[], feature_names='', 
                                     step_size_list = [0.05, 0.1, 0.5, 1, 5, 10, 50],
                                     class_label='',no_of_points=5):
    """
    Args:
        training_data: numpy 2d array. Training data should have categorical columns label encoded.
            But they shouldn't be one-hot encoded or any other encoding which makes multiple columns out 
            of one categorical column.
        data_row: 1d numpy array, corresponding to a row
        columns: list of column numbers whose neighbourhood plot you wanna see. Default is all columns.
            This cannot be an empty list.
        predict_fn: prediction function. For classifiers, this should be a function that takes a numpy 
            array and outputs prediction probabilities. For regressors, this takes a numpy array and 
            returns the predictions. For ScikitClassifiers, this is `classifier.predict_proba()`. For 
            ScikitRegressors, this is `regressor.predict()`. This function takes encoded data as an 
            input (if encoding is used) and 
        categorical_names_encoder: it is a dictionary with keys as the categorical column no. for which 
            the encoder is for and the value is a function which takes a category as input and outputs 
            the encoded value of it which can be fed to the prediction function.
        encode_fn: a function which takes input as the categorical name encoder and category and outputs
            the encoded value
        categorical_names: map from int to list of names, where
            categorical_names[x][y] represents the name of the yth value of
            column x.
        categorical_features: list of indices (ints) corresponding to the
            categorical columns. Everything else will be considered
            continuous. Values in these columns MUST be integers.
        feature_names: list of names (strings) corresponding to the columns
            in the training data.
        step_size_list: list of percentile steps to be taken while changing the value of a certain 
            continuous feature. If first percentile step gives the same predict_fn output value 
            then next value in this list will be triwd. Elements of lit should be in the range of 0 to 100.
            Default: [0.05, 0.1, 0.5, 1, 5, 10, 50]
        class_label: Should not be '' in case of a classifier otherwise model will be considered as a 
            regressor. In case of a classifier class_label should be of the class of interest whose 
            probabilities will be returned. class_label can only be the allowable indexes of the array 
            of probabilities returned by predict_fn in case of a classifier.
        no_of_points: no. of points on each side of the column value of the input data_row. If the predict_fn 
            output value doesn't change after a certain point then no. of points returned can be less than
            this value.
        output_type: 'list' or 'plot'. Default value is 'plot'.
        
        Returns:
            a dictionary with keys as column numbers and it's values as 3 lists:
            1) List of values for that columns
            2) predict_fn output for those values
            3) list of flag with value 1 for original predictor value, 0 for all others
        
    """
    temp_data_row = data_row.copy()
    
    output_dict = dict()
    
    for column_no in  columns:
        
        predictor_values = list()
        output_values = list()
        is_original_value = list()
    
        data_column = pd.Series(train_data[:,column_no])

        if column_no in categorical_features:
            for category in categorical_names[column_no]:
                if data_row[column_no] == encode_fn(categorical_names_encoder[column_no], category):
                    is_original_value.append(1)
                else:
                    is_original_value.append(0)
                temp_data_row[column_no] = encode_fn(categorical_names_encoder[column_no], category)
                predictor_values.append(category)
                if class_label != '':
                    output_values.append(predict_fn(temp_data_row.reshape(1, -1))[class_label])
                else:
                    output_values.append(predict_fn(temp_data_row.reshape(1, -1)))
        else:
            sorted_column = list(np.sort(data_column))

            predictor_value = data_row[column_no]
            if class_label != '':
                output_value = predict_fn(data_row.reshape(1, -1))[class_label]
            else:
                output_value = predict_fn(data_row.reshape(1, -1))
            data_column_unique = data_column.unique()
            no_of_unique_values = len(data_column_unique)



            for i in range(no_of_points):
                if predictor_value != min(data_column):
                    percentile = stats.percentileofscore(data_column_unique, predictor_value, kind='strict')

                    for step_size in step_size_list:
                        if percentile >= step_size:
                            predictor_value_temp = np.percentile(data_column_unique, percentile-step_size, 
                                                                 interpolation='lower')
                            temp_data_row[column_no] = predictor_value_temp
                            if class_label != '':
                                output_value_temp = predict_fn(temp_data_row.reshape(1, -1))[class_label]
                            else:
                                output_value_temp = predict_fn(temp_data_row.reshape(1, -1))
                            if output_value_temp == output_value:
                                continue
                            else:
                                output_value = output_value_temp
                                predictor_value = predictor_value_temp

                                predictor_values.append(predictor_value)
                                output_values.append(output_value)

                                break
                        else:
                            predictor_value = np.percentile(data_column_unique, 0)
                            predictor_values.append(predictor_value)

                            temp_data_row[column_no] = predictor_value

                            if class_label != '':
                                output_value = predict_fn(temp_data_row.reshape(1, -1))[class_label]
                            else:
                                output_value = predict_fn(temp_data_row.reshape(1, -1))
                            output_values.append(output_value)

                            break
                else:
                    break

            no_of_points_on_left = len(predictor_values)
            is_original_value = [0]*no_of_points_on_left
            is_original_value.append(1)

            predictor_value = data_row[column_no]
            predictor_values.append(predictor_value)

            if class_label != '':
                output_value = predict_fn(data_row.reshape(1, -1))[class_label]
            else:
                output_value = predict_fn(data_row.reshape(1, -1))
            output_values.append(output_value)

            for i in range(no_of_points):
                if predictor_value != max(data_column):
                    percentile = stats.percentileofscore(data_column_unique, predictor_value, kind='strict')

                    for step_size in step_size_list:
                        if percentile <= 100 - step_size:
                            predictor_value_temp = np.percentile(data_column_unique, percentile+step_size, 
                                                                 interpolation='higher')
                            temp_data_row[column_no] = predictor_value_temp
                            if class_label != '':
                                output_value_temp = predict_fn(temp_data_row.reshape(1, -1))[class_label]
                            else:
                                output_value_temp = predict_fn(temp_data_row.reshape(1, -1))

                            if output_value_temp == output_value:
                                continue
                            else:
                                output_value = output_value_temp
                                predictor_value = predictor_value_temp

                                predictor_values.append(predictor_value)
                                output_values.append(output_value)

                                break
                        else:
                            predictor_value = np.percentile(data_column_unique, 100)
                            predictor_values.append(predictor_value)

                            temp_data_row[column_no] = predictor_value

                            if class_label != '':
                                output_value = predict_fn(temp_data_row.reshape(1, -1))[class_label]
                            else:
                                output_value = predict_fn(temp_data_row.reshape(1, -1))
                            output_values.append(output_value)

                            break
                else:
                    break

            is_original_value = is_original_value + [0]*(len(predictor_values)-no_of_points_on_left-1)

        if len(feature_names) != 0:
            output_dict[feature_names[column_no]] = predictor_values, output_values, is_original_value
        else:
            output_dict[column_no] = predictor_values, output_values, is_original_value
        
    return output_dict


# In[ ]:



