from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3
import logging
import os
import json
from app.config import Config
from app.models import init_db, create_user, get_all_users, get_user_by_id
from app.utils import validate_user_data, setup_logging

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize database
init_db()

@app.before_request
def log_request_info():
    """Log incoming requests"""
    logger.info(f"Request: {request.method} {request.url}")

@app.after_request
def after_request(response):
    """Add security headers"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/', methods=['GET'])
def welcome():
    """Welcome endpoint with API information"""
    try:
        return jsonify({
            "message": "Welcome to DevOps Flask API",
            "version": "1.0.0",
            "description": "Complete CI/CD Pipeline with LocalStack and GitHub Actions",
            "endpoints": {
                "health": "/health",
                "users": "/api/v1/users",
                "info": "/api/v1/info",
                "docs": "/api/v1/docs"
            },
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error in welcome endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint with detailed metrics"""
    try:
        # Check database connectivity
        db_status = "healthy"
        try:
            conn = sqlite3.connect(app.config['DATABASE_PATH'])
            conn.execute("SELECT 1")
            conn.close()
        except Exception as e:
            db_status = f"unhealthy: {str(e)}"
            logger.warning(f"Database health check failed: {str(e)}")

        health_data = {
            "status": "healthy" if db_status == "healthy" else "degraded",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "services": {
                "database": db_status,
                "api": "healthy"
            },
            "uptime": "Service running",
            "environment": app.config['ENV']
        }
        
        status_code = 200 if health_data["status"] == "healthy" else 503
        return jsonify(health_data), status_code
        
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 503

@app.route('/api/v1/users', methods=['GET', 'POST'])
def users():
    """Users endpoint for CRUD operations"""
    try:
        if request.method == 'GET':
            # Get all users
            users_data = get_all_users()
            return jsonify({
                "users": users_data,
                "count": len(users_data),
                "timestamp": datetime.utcnow().isoformat()
            }), 200
            
        elif request.method == 'POST':
            # Create new user
            data = request.get_json()
            
            # Validate input
            validation_error = validate_user_data(data)
            if validation_error:
                return jsonify({"error": validation_error}), 400
            
            # Create user
            user_id = create_user(data['name'], data['email'])
            
            return jsonify({
                "message": "User created successfully",
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }), 201
            
    except Exception as e:
        logger.error(f"Error in users endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get specific user by ID"""
    try:
        user = get_user_by_id(user_id)
        if user:
            return jsonify({
                "user": user,
                "timestamp": datetime.utcnow().isoformat()
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404
            
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/v1/info', methods=['GET'])
def info():
    """Application metadata and system information"""
    try:
        return jsonify({
            "application": {
                "name": "DevOps Flask API",
                "version": "1.0.0",
                "description": "Complete CI/CD Pipeline with LocalStack",
                "author": "DevOps Team",
                "framework": "Flask"
            },
            "system": {
                "python_version": "3.9+",
                "environment": app.config['ENV'],
                "debug_mode": app.config['DEBUG']
            },
            "features": [
                "CI/CD Pipeline",
                "LocalStack Integration",
                "Terraform IaC",
                "SQLite Database",
                "API Documentation",
                "Health Monitoring",
                "Structured Logging"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in info endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/v1/docs', methods=['GET'])
def api_docs():
    """API documentation endpoint"""
    try:
        docs = {
            "openapi": "3.0.0",
            "info": {
                "title": "DevOps Flask API",
                "version": "1.0.0",
                "description": "Complete CI/CD Pipeline API"
            },
            "paths": {
                "/": {
                    "get": {
                        "summary": "Welcome message",
                        "responses": {"200": {"description": "Welcome information"}}
                    }
                },
                "/health": {
                    "get": {
                        "summary": "Health check",
                        "responses": {"200": {"description": "Service health status"}}
                    }
                },
                "/api/v1/users": {
                    "get": {
                        "summary": "Get all users",
                        "responses": {"200": {"description": "List of users"}}
                    },
                    "post": {
                        "summary": "Create new user",
                        "responses": {"201": {"description": "User created"}}
                    }
                },
                "/api/v1/info": {
                    "get": {
                        "summary": "Application information",
                        "responses": {"200": {"description": "App metadata"}}
                    }
                }
            }
        }
        return jsonify(docs), 200
        
    except Exception as e:
        logger.error(f"Error in docs endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested resource does not exist",
        "timestamp": datetime.utcnow().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred",
        "timestamp": datetime.utcnow().isoformat()
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
