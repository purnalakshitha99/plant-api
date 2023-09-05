from flask import Blueprint, jsonify, request
import numpy as np
import tensorflow as tf
import pipe.plant_prediction_pipeline as prediction
from application import db
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

config = tf.compat.v1.ConfigProto(device_count={'GPU': 0})
sess = tf.compat.v1.Session(config=config)

plant_prediction_controller = Blueprint('plant_prediction', __name__)

predicted_collection = db["predicted_lists"]

@plant_prediction_controller.route("/plant", methods = ['POST'])
def plantPrediction():
    if request.method == "POST":
        data = request.json
        image_url = data['image_url']
        print(image_url)
        ans=prediction.plant_recognition(image_url)

        test_set = tf.keras.utils.image_dataset_from_directory(
            'models/test',
            labels = 'inferred',
            label_mode = 'categorical',
            class_names = None,
            color_mode ='rgb',
            batch_size = 32,
            image_size = (64, 64),
            shuffle = True,
            seed = None,
            validation_split= None,
            subset = None,
            interpolation = 'bilinear',
            follow_links = False,
            crop_to_aspect_ratio = False
        )

        test_set.class_names

        result_index = np.where(ans[0] == max(ans[0]))
        print(result_index[0][0])

        print("It's a {}".format(test_set.class_names[result_index[0][0]]))
        response_data = {
            "result_index": test_set.class_names[result_index[0][0]],
        }
        return jsonify(response_data)

@plant_prediction_controller.route("/save", methods=['POST'])
def save_prediction():
    data = request.json
    user_id = data['user_id']
    url = data['image_url']
    predicted_name = data['predicted_name']
    predicted_week = data['predicted_week']
    # password = data['password']

    new_item = {"user_id": user_id, "url":url,"predicted_name": predicted_name, "predicted_week":predicted_week }
    predicted_collection.insert_one(new_item)
    new_item["_id"] = str(new_item["_id"])
    return jsonify(new_item), 201


@plant_prediction_controller.route("/", methods = ['GET'])
def get_predictions():
    predictions = []
    for qanda in predicted_collection.find():
        qanda["_id"] = str(qanda["_id"])
        print(qanda)
        predictions.append(qanda)
    return jsonify(predictions)