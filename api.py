from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data representing locations and facilities in a railway station
station_data = {
    "ticket_counter": {"location": "Block A", "coordinates": [25.435, 81.846]},
    "food_courts": {"location": "Block B", "coordinates": [25.436, 81.847]},
    "waiting_rooms": {"location": "Block C", "coordinates": [25.437, 81.848]},
    "parking_area": {"location": "Entry Gate", "coordinates": [25.438, 81.849]},
    "rpf_support": {"location": "Security Office", "coordinates": [25.439, 81.850]},
    "station_master": {"location": "Admin Block", "coordinates": [25.440, 81.851]},
    "report_missing": {"location": "Help Desk", "coordinates": [25.441, 81.852]},
    "train_schedule": {"display": "Main Hall Screen"},
}

# Home route
@app.route('/')
def home():
    return "Railway Station Navigation API"

# Get list of all facilities
@app.route('/facilities', methods=['GET'])
def get_facilities():
    return jsonify({"facilities": list(station_data.keys())})

# Get info of a specific facility
@app.route('/facility/<string:name>', methods=['GET'])
def get_facility(name):
    facility = station_data.get(name.lower())
    if facility:
        return jsonify({name: facility})
    else:
        return jsonify({"error": "Facility not found"}), 404

# Add or update facility info
@app.route('/facility/<string:name>', methods=['POST'])
def update_facility(name):
    data = request.json
    station_data[name.lower()] = data
    return jsonify({"message": f"{name} data updated successfully"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
