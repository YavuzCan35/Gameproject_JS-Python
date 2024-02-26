import random
from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Initial marker position
marker_lat = 40.0
marker_lng = -80.0

# Serve the map.html template
@app.route('/')
def index():
    return render_template('players_map.html')

# API endpoint to get the marker's position
@app.route('/get_marker_position', methods=['GET'])
def get_marker_position():
    global marker_lat, marker_lng
    # Change marker's coordinates with random values
    marker_lat  +=0.01
    marker_lng +=0.01
    return jsonify({'lat': marker_lat, 'lng': marker_lng})

if __name__ == '__main__':
    app.run(debug=True)
