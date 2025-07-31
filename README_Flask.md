# Flask Backend for AI Floor Plan Generator

This Flask backend provides the API endpoints for the AI Floor Plan Generator application.

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Flask Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. Update Frontend Configuration

Make sure your frontend is configured to make requests to the Flask backend. The current setup expects the backend to be running on port 5000.

## API Endpoints

### POST /generate-floorplan
Generates a floor plan based on user input.

**Request Body:**
```json
{
  "sqft": 2000,
  "depth": 60,
  "width": 40,
  "directions": "North facing",
  "bathrooms": "Standard",
  "masterbedroom": "Spacious",
  "masterbedrooms": "2",
  "floors": "Ground + 1st Floor",
  "garden": "Yes",
  "varanda": "Yes",
  "design": "Modern Contemporary",
  "description": "Dream home with modern amenities"
}
```

**Response:**
```json
{
  "success": true,
  "image_url": "URL_TO_GENERATED_IMAGE",
  "message": "Floor plan generated successfully"
}
```

### GET /health
Health check endpoint to verify the server is running.

### GET /api/test
Test endpoint to verify the API is working.

## Integration with AI Services

The current implementation includes a mock AI service. To integrate with your actual AI service:

1. Replace the `generate_floor_plan_with_ai()` function in `app.py`
2. Add your AI service API credentials to environment variables
3. Install any additional dependencies required by your AI service

## Example AI Service Integration

```python
def generate_floor_plan_with_ai(data):
    # Example integration with OpenAI, Stability AI, or custom AI service
    response = requests.post(
        'YOUR_AI_SERVICE_ENDPOINT',
        headers={
            'Authorization': f'Bearer {YOUR_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'prompt': f"Generate a floor plan for a {data['sqft']} sqft house...",
            'parameters': data
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        return {
            "success": True,
            "image_url": result.get('image_url'),
            "message": "Floor plan generated successfully"
        }
    else:
        return {
            "success": False,
            "error": "AI service unavailable"
        }
```

## Environment Variables

Create a `.env` file for sensitive configuration:

```
AI_SERVICE_API_KEY=your_api_key_here
AI_SERVICE_ENDPOINT=https://api.your-ai-service.com/generate
DEBUG=True
```

## Production Deployment

For production deployment:

1. Set `debug=False` in `app.run()`
2. Use a production WSGI server like Gunicorn
3. Set up proper environment variables
4. Configure CORS settings for your domain
5. Add proper error logging and monitoring

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```