#!/usr/bin/env python3
"""
Flask app example demonstrating spewer debugging functionality.
"""

from flask import Flask, request, jsonify
from spewer import SpewContext, spew, unspew
import json
import time

app = Flask(__name__)

# Global variable to track request count
request_count = 0

def process_data(data):
    """Process incoming data with some calculations."""
    result = 0
    for item in data:
        if isinstance(item, (int, float)):
            result += item
        elif isinstance(item, str):
            result += len(item)
    return result

def validate_input(data):
    """Validate input data."""
    if not isinstance(data, list):
        return False, "Data must be a list"
    if len(data) == 0:
        return False, "Data cannot be empty"
    return True, "Valid"

@app.route('/')
def home():
    """Home route with basic response."""
    global request_count
    request_count += 1
    
    # Use spewer to debug this function
    with SpewContext(show_values=True):
        message = f"Welcome to Flask Spewer Demo! Request #{request_count}"
        response = {"message": message, "request_count": request_count}
        return jsonify(response)

@app.route('/debug', methods=['POST'])
def debug_endpoint():
    """Endpoint that demonstrates spewer debugging."""
    global request_count
    request_count += 1
    
    # Start spewer for this request
    spew(show_values=True)
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input
        is_valid, message = validate_input(data)
        
        if not is_valid:
            unspew()
            return jsonify({"error": message}), 400
        
        # Process the data
        result = process_data(data)
        
        # Create response
        response = {
            "result": result,
            "input_length": len(data),
            "request_count": request_count,
            "timestamp": time.time()
        }
        
        unspew()
        return jsonify(response)
        
    except Exception as e:
        unspew()
        return jsonify({"error": str(e)}), 500

@app.route('/simple')
def simple_endpoint():
    """Simple endpoint without spewer for comparison."""
    global request_count
    request_count += 1
    
    return jsonify({
        "message": "Simple endpoint - no debugging",
        "request_count": request_count
    })

@app.route('/context-debug', methods=['POST'])
def context_debug_endpoint():
    """Endpoint using context manager for spewer."""
    global request_count
    request_count += 1
    
    with SpewContext(show_values=True):
        data = request.get_json()
        
        # Validate input
        is_valid, message = validate_input(data)
        
        if not is_valid:
            return jsonify({"error": message}), 400
        
        # Process the data
        result = process_data(data)
        
        # Create response
        response = {
            "result": result,
            "input_length": len(data),
            "request_count": request_count,
            "timestamp": time.time()
        }
        
        return jsonify(response)

@app.route('/module-debug', methods=['POST'])
def module_debug_endpoint():
    """Endpoint with module-specific debugging."""
    global request_count
    request_count += 1
    
    # Only debug the main module
    spew(trace_names=['__main__'], show_values=True)
    
    try:
        data = request.get_json()
        is_valid, message = validate_input(data)
        
        if not is_valid:
            unspew()
            return jsonify({"error": message}), 400
        
        result = process_data(data)
        
        response = {
            "result": result,
            "input_length": len(data),
            "request_count": request_count,
            "timestamp": time.time()
        }
        
        unspew()
        return jsonify(response)
        
    except Exception as e:
        unspew()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask app with spewer debugging...")
    print("Available endpoints:")
    print("  GET  / - Home page")
    print("  POST /debug - Debug endpoint with manual spew/unspew")
    print("  GET  /simple - Simple endpoint (no debugging)")
    print("  POST /context-debug - Debug endpoint with context manager")
    print("  POST /module-debug - Debug endpoint with module filtering")
    print("\nTest with curl:")
    print('  curl -X POST http://localhost:5000/debug -H "Content-Type: application/json" -d \'[1, 2, 3, "hello"]\'')
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000) 