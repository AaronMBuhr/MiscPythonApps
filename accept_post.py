import argparse
from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/<path:dynamic_path>', methods=['POST'])
def post(dynamic_path):
    print(f"Received POST request on /{dynamic_path}:")
    json_payload = json.dumps(request.json)  # Convert dict back to JSON string
    print(json_payload)  # This will print with double quotes
    return f"POST request received on /{dynamic_path}!", 200

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the Flask app.")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on")
    args = parser.parse_args()
    
    app.run(debug=True, port=args.port)
