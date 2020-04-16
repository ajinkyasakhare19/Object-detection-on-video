import tensorflow as tf
import keras
from keras.preprocessing import image
from keras.initializers import glorot_uniform
import numpy as np
import cv2

import os
import csv

IMG_SIZE = 224
color = {}
class DetectCartype():
    def __init__(self,model_json="./cartype_model_data/cartype_model_v2.json",  weights_h5="./cartype_model_data/cartype_weights_v2.h5"):
        self.model_json = model_json #cartype_model.json
        self.weights_h5 = weights_h5 #cartype_weights.h5
        self.model = self.load_model()

    def load_model(self):
        #Reading the model from JSON file
        with open(self.model_json, 'r') as json_file:
            json_savedModel= json_file.read()
        #load the model architecture 
        model_j = tf.keras.models.model_from_json(json_savedModel)
        model_j.summary()
        model_j.load_weights(self.weights_h5)
        return model_j
    
    def predict_cartype(self,in_img):
        img = cv2.resize(in_img,(IMG_SIZE,IMG_SIZE))
        img_tensor = image.img_to_array(img)                    # (height, width, channels)
        img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
        img_tensor /= 255.                                      # imshow expects values in the range [0, 1]
        pred = self.model.predict(img_tensor)
        if pred[0][0] < 0.95:
            type = "Hatchback"
        else:
            type = "Sedan"
        
        return type
    
    
            

