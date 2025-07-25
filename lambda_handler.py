import json
import base64
from urllib.parse import unquote_plus

try:
    from app import app
except ImportError:
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return {'message': 'Hello from Lambda!'}

def lambda_handler(event, context):
    """
    AWS Lambda handler for Flask application
    """
    
    # Extract HTTP method and path
    http_method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    
    # Extract query parameters
    query_params = event.get('queryStringParameters') or {}
    
    # Extract headers
    headers = event.get('headers') or {}
    
    # Extract body
    body = event.get('body', '')
    if event.get('isBase64Encoded', False):
        body = base64.b64decode(body).decode('utf-8')
    
    try:
        # Test the Flask app
        with app.test_client() as client:
            if http_method == 'GET':
                response = client.get(path, query_string=query_params, headers=headers)
            elif http_method == 'POST':
                response = client.post(path, data=body, query_string=query_params, headers=headers)
            elif http_method == 'PUT':
                response = client.put(path, data=body, query_string=query_params, headers=headers)
            elif http_method == 'DELETE':
                response = client.delete(path, query_string=query_params, headers=headers)
            else:
                response = client.open(path, method=http_method, data=body, query_string=query_params, headers=headers)
            
            # Prepare response
            response_headers = {}
            for key, value in response.headers:
                response_headers[key] = value
            
            # Handle response body
            response_body = response.get_data(as_text=True)
            
            return {
                'statusCode': response.status_code,
                'headers': response_headers,
                'body': response_body,
                'isBase64Encoded': False
            }
            
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Internal server error', 'message': str(e)})
        }
