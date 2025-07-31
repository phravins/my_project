from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
import time
import random
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
UPLOAD_FOLDER = 'generated_plans'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Mock AI service - Replace this with your actual AI service
def generate_floor_plan_with_ai(data):
    """
    Replace this function with your actual AI floor plan generation logic.
    This is a mock implementation that simulates AI processing.
    """
    try:
        # Simulate AI processing time
        time.sleep(2)
        
        # Mock response - replace with actual AI service call
        # Example of how you might call an actual AI service:
        # response = requests.post('YOUR_AI_SERVICE_URL', json=data)
        # return response.json()
        
        # For now, return a mock success response
        # You should replace this with actual AI-generated image URL
        mock_image_url = "https://via.placeholder.com/800x600/4A90E2/FFFFFF?text=AI+Generated+Floor+Plan"
        
        return {
            "success": True,
            "image_url": mock_image_url,
            "message": "Floor plan generated successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"AI generation failed: {str(e)}"
        }

@app.route('/')
def index():
    """Serve the main application"""
    return send_from_directory('dist', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from the dist directory"""
    return send_from_directory('dist', path)

@app.route('/generate-floorplan', methods=['POST'])
def generate_floorplan():
    """Generate floor plan using AI based on user input"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Validate required fields
        required_fields = ['sqft', 'depth', 'width']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return jsonify({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        # Log the received data for debugging
        print(f"Received floor plan request: {json.dumps(data, indent=2)}")
        
        # Process the data and generate floor plan
        result = generate_floor_plan_with_ai(data)
        
        # Log the result
        print(f"AI generation result: {json.dumps(result, indent=2)}")
        
        # Save request data for future reference
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        request_file = os.path.join(app.config['UPLOAD_FOLDER'], f'request_{timestamp}.json')
        
        with open(request_file, 'w') as f:
            json.dump({
                'timestamp': timestamp,
                'request_data': data,
                'result': result
            }, f, indent=2)
        
        return jsonify(result)
        
    except Exception as e:
        error_message = f"Server error: {str(e)}"
        print(f"Error in generate_floorplan: {error_message}")
        
        return jsonify({
            "success": False,
            "error": error_message
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "AI Floor Plan Generator"
    })

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    """Test endpoint to verify API is working"""
    return jsonify({
        "message": "Flask backend is working!",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Available endpoints:")
    print("  GET  /health - Health check")
    print("  GET  /api/test - Test endpoint")
    print("  POST /generate-floorplan - Generate floor plan")
    print("  GET  / - Serve frontend application")
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )