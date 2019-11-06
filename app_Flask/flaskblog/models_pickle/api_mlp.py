from flask import Flask, jsonify, request
import numpy as np
import os
import pickle
import tensorflow as tf 
import numpy as np
from sklearn.preprocessing import StandardScaler
global graph
from flask import copy_current_request_context

sc = StandardScaler()


app = Flask(__name__)


################# NN model #####################
def baseline_model(optimizer='adam'):
    # create model
    model = Sequential()
    model.add(Dense(7, input_dim=7, kernel_initializer='normal', activation='relu'))
    model.add(Dense(6, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, activation='linear',kernel_regularizer = 'l2',  kernel_initializer='normal'))
    model.compile(loss='mse', optimizer=optimizer, metrics=['mse', 'mae', 'mape', 'cosine'])
    return model
    

@app.route('/predict',methods=['POST'])
def predict():
    data = request.get_json()['list']
    print("********************", data)
    with graph.as_default():    
        pred=scaler.transform(data)
        result = model_NN.predict(pred)
        print(result.tolist())
    return jsonify(result.tolist())


@app.route('/predict_pr',methods=['POST'])
def predict_pr():
    data = request.get_json()['list']
    result=model_poly_reg.predict(poly_features.fit_transform(data))
    return jsonify(result.tolist())

@app.route('/predict_rf',methods=['POST'])
##############  Random forest  ################
def predict_rf():
    data = request.get_json()['list']
    result = model_rf.predict(sc.fit_transform(data))
    return jsonify(result.tolist())


if __name__ == '__main__':
    graph = tf.get_default_graph()

    # Loading NN model
    path_NN = 'NN.pickle'
    path_NN_scaler = 'NN_scaler.pickle'
    model_NN = pickle.load(open(path_NN, 'rb'))
    scaler=pickle.load(open(path_NN_scaler, 'rb'))
    # Loading Polynomial regression
    path_poly_reg = 'Polynomial_regression.pickle'
    path_poly_features = 'Polynomial_features.pickle'
    model_poly_reg = pickle.load(open(path_poly_reg, 'rb'))
    poly_features  = pickle.load(open(path_poly_features , 'rb'))
    # Loading Polynomial regression
    path_rf = 'Random_forest .pickle'
    model_rf = pickle.load(open(path_rf, 'rb'))

    app.run(debug=True, port=12347)
 