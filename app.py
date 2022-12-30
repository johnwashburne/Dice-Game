from prediction_engine.distribution_loader import DistributionLoader
from prediction_engine.predictor import Predictor
from flask import Flask, request, jsonify

app = Flask(__name__)
p = Predictor(DistributionLoader.load("default"))


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    data = request.get_json()
    current_points = data['current_points']
    score_to_beat = data['score_to_beat']
    opponents_left = data['opponents_left']
    dice = data['dice']

    dice_to_keep, probability = p.optimize_turn(
        current_points, score_to_beat, opponents_left, dice)

    response = jsonify({
        "dice": dice_to_keep,
        "probability": probability
    })
    return response
