from flask import Blueprint, jsonify, request
import numpy as np
import tensorflow as tf
import pipe.plant_type_and_week_pipeline as prediction_name_week

plant_type_and_week_controller = Blueprint('plant_type_and_week_controller', __name__)

@plant_type_and_week_controller.route("/plant_week", methods = ['POST'])
def plant_week_Prediction():
    if request.method == "POST":
        data = request.json
        image_url = data['image_url']
        print(image_url)
        predicted_type,predicted_week_rounded=prediction_name_week.plantname_and_week_recognition(image_url)
        print(f"Predicted Plant Type: {predicted_type}")
        print(f"Predicted Growth Stage (Week): {predicted_week_rounded}")
        prediction_data = {
        "type": predicted_type,
        "week": predicted_week_rounded
        }
        return jsonify( message = prediction_data)
