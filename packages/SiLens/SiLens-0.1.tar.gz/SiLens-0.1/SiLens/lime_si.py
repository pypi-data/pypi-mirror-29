import lime
import lime.lime_tabular

def explain_instance_si(training_data, data_row, predict_fn, label, mode='classification', training_labels=None,
                        feature_names=None, categorical_features=None, categorical_names=None, kernel_width=None,
                        verbose=False, class_names=None, feature_selection='auto', discretize_continuous=True,
                        discretizer='quartile', labels=(1, ), top_labels=None, num_features=10, num_samples=5000, 
                        distance_metric='euclidean', model_regressor=None):

    """
    Args:
        training_data: numpy 2d array
        mode: "classification" or "regression"
        training_labels: labels for training data. Not required, but may be
            used by discretizer.
        feature_names: list of names (strings) corresponding to the columns
            in the training data.
        categorical_features: list of indices (ints) corresponding to the
            categorical columns. Everything else will be considered
            continuous. Values in these columns MUST be integers.
        categorical_names: map from int to list of names, where
            categorical_names[x][y] represents the name of the yth value of
            column x.
        kernel_width: kernel width for the exponential kernel.
            If None, defaults to sqrt (number of columns) * 0.75
        verbose: if true, print local prediction values from linear model
        class_names: list of class names, ordered according to whatever the
            classifier is using. If not present, class names will be '0',
            '1', ...
        feature_selection: feature selection method. can be
            'forward_selection', 'lasso_path', 'none' or 'auto'.
            See function 'explain_instance_with_data' in lime_base.py for
            details on what each of the options does.
        discretize_continuous: if True, all non-categorical features will
            be discretized into quartiles.
        discretizer: only matters if discretize_continuous is True. Options
            are 'quartile', 'decile', 'entropy' or a BaseDiscretizer
            instance.
        random_state: an integer or numpy.RandomState that will be used to
            generate random numbers. If None, the random state will be
            initialized using the internal numpy seed.
        
        data_row: 1d numpy array, corresponding to a row
        predict_fn: prediction function. For classifiers, this should be a
            function that takes a numpy array and outputs prediction
            probabilities. For regressors, this takes a numpy array and
            returns the predictions. For ScikitClassifiers, this is
            `classifier.predict_proba()`. For ScikitRegressors, this
            is `regressor.predict()`. The prediction function needs to work
            on multiple feature vectors (the vectors randomly perturbed
            from the data_row).
        labels: iterable with labels to be explained.
        top_labels: if not None, ignore labels and produce explanations for
            the K labels with highest prediction probabilities, where K is
            this parameter.
        num_features: maximum number of features present in explanation
        num_samples: size of the neighborhood to learn the linear model
        distance_metric: the distance metric to use for weights.
        model_regressor: sklearn regressor to use in explanation. Defaults
            to Ridge regression in LimeBase. Must have model_regressor.coef_
            and 'sample_weight' as a parameter to model_regressor.fit()    
        
        Returns:
            list of tuples (representation, weight), where representation is
            given by domain_mapper. Weight is a float.
        
    """
    
    explainer = lime.lime_tabular.LimeTabularExplainer(training_data=training_data ,feature_names = feature_names,
                                                       class_names=class_names, categorical_features=categorical_features,
                                                       categorical_names=categorical_names, kernel_width=kernel_width,
                                                       mode=mode, training_labels=training_labels,verbose=verbose,
                                                       feature_selection=feature_selection,
                                                       discretize_continuous=discretize_continuous,
                                                       discretizer=discretizer)


    exp = explainer.explain_instance(data_row=data_row, predict_fn=predict_fn, labels=labels, top_labels=top_labels,
                                     num_features=num_features, num_samples=num_samples,distance_metric=distance_metric,
                                     model_regressor=model_regressor)

    explanation = exp.as_list(label=label)
    
    return explanation

