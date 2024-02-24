import random
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Initial marker position
marker_lat = 39.9208
marker_lng = 32.8541

# Serve the map.html template
@app.route('/')
def index():
    return render_template('map.html')

# Initial data for markers, corresponding to the cities in your Folium map
markers = {
    '1': {'lat': 41.0082, 'lng': 28.9784, 'city': 'Istanbul'},
    '2': {'lat': 39.9334, 'lng': 32.8597, 'city': 'Ankara'},
    '3': {'lat': 38.4192, 'lng': 27.1287, 'city': 'Izmir'},
    '4': {'lat': 40.1826, 'lng': 29.0669, 'city': 'Bursa'},
    '5': {'lat': 36.8969, 'lng': 30.7133, 'city': 'Antalya'},
}

@app.route('/get_markers')
def get_markers():
    # Simulate marker position changes
    for marker in markers.values():
        marker['lat'] += random.uniform(-0.01, 0.01)  # Small random latitude adjustment
        marker['lng'] += random.uniform(-0.01, 0.01)  # Small random longitude adjustment
    return jsonify(markers)


# API endpoint to update the marker's position
@app.route('/update_marker_position', methods=['POST'])
def update_marker_position():
    global marker_lat, marker_lng
    data = request.json
    print(data)
    marker_lat = data['lat']
    marker_lng = data['lng']
    return jsonify({'lat': marker_lat, 'lng': marker_lng})



from math import sin, cos, sqrt, atan2, radians

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # approximate radius of Earth in km

    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def calculate_route_length(coordinates):
    route_length = 0

    for i in range(len(coordinates) - 1):
        lat1, lon1 = coordinates[i]['lat'], coordinates[i]['lng']
        lat2, lon2 = coordinates[i + 1]['lat'], coordinates[i + 1]['lng']

        distance = haversine_distance(lat1, lon1, lat2, lon2)
        route_length += distance

    return route_length
# Route to receive the array of coordinates from the map.html
@app.route('/update_recorded_locations', methods=['POST'])
def update_recorded_locations():
    global recorded_locations
    data = request.get_json()
    print(data)
    if 'coordinates' in data:
        recorded_locations = data['coordinates']
        print("Received recorded locations:", recorded_locations)
        route_length = calculate_route_length(recorded_locations)
        print("Route length:", route_length, "km")

        print(len(recorded_locations))
        print("Received recorded locations:", recorded_locations)
        return jsonify(message="Recorded locations received successfully"), 200
    else:
        return jsonify(error="Invalid data"), 400

if __name__ == '__main__':
    app.run(debug=True)
