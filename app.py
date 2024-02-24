from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/send-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    print(data)
    print(f"Received data from the client")
    return jsonify({'message': 'Data received successfully'})

if __name__ == '__main__':
    app.run(debug=True)
