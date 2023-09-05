import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os
import tensorflow as tf
import requests
from PIL import Image

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

config = tf.compat.v1.ConfigProto(device_count={'GPU': 0})
sess = tf.compat.v1.Session(config=config)

def plantname_and_week_recognition(image_url):

    # Load the trained model
    model = load_model('models/plant_type_and_week_model.h5')

    plant_categories = ['Eggplant', 'Penaga_Laut', 'Terminalia_Catappa', 'Plant Unknown']

    # Load and preprocess the new image
    image_path = image_url

    response = requests.get(image_url)
    with open('temp_image.jpg', 'wb') as f:
        f.write(response.content)

    img = cv2.imread('temp_image.jpg')
    img = cv2.resize(img, (128, 128))  # Resize to 128x128 pixels
    img = np.expand_dims(img, axis=0)  # Add a batch dimension

    # Make predictions
    type_pred, week_pred = model.predict(img)

    # Get the predicted plant type and week
    predicted_type_index = np.argmax(type_pred)
    predicted_type = plant_categories[predicted_type_index]
    predicted_week = week_pred[0][0]  # Extract the week value from the 2D array

    # Round the predicted week to the nearest whole number
    predicted_week_rounded = round(predicted_week)

    # Get the confidence score for the plant type prediction
    confidence_score = type_pred[0][predicted_type_index] * 100  # Convert to percentage

    # Display the predictions and confidence score
    print(f"Predicted Plant Type: {predicted_type} (Confidence: {confidence_score:.2f}%)")
    print(f"Predicted Growth Stage (Week): {predicted_week_rounded}")

    return predicted_type,predicted_week_rounded

