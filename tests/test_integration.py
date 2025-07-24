import pytest
import requests
import time
import subprocess
import os

class TestIntegration:
    """Integration tests for the complete pipeline"""
    
    @pytest.fixture(scope="class", autouse=True)
    def setup_localstack(self):
        """Start LocalStack for integration tests"""
        # Start LocalStack
        subprocess.run(['docker-compose', 'up', '-d', 'localstack'], check=True)
        
        # Wait for LocalStack to be ready
        for _ in range(30):
            try:
                response = requests.get('http://localhost:4566/_localstack/health')
                if response.status_code == 200:
                    break
            except requests.exceptions.RequestException:
                pass
            time.sleep(2)
        else:
            pytest.fail("LocalStack failed to start")
        
        yield
        
        # Cleanup
        subprocess.run(['docker-compose', 'down'], check=False)
    
    def test_localstack_health(self):
        """Test that LocalStack is running and healthy"""
        response = requests.get('http://localhost:4566/_localstack/health')
        assert response.status_code == 200
        
        health_data = response.json()
        assert 'services' in health_data
    
    def test_terraform_deployment(self):
        """Test Terraform deployment to LocalStack"""
        # Create a simple lambda package for testing
        os.makedirs('test-lambda', exist_ok=True)
        
        with open('test-lambda/lambda_function.py', 'w') as f:
            f.write('''
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': '{"message": "Hello from Lambda"}'
    }
''')
        
        # Create zip file
        subprocess.run(['zip', '-r', 'test-lambda.zip', 'test-lambda/'], check=True)
        
        # Run terraform
        os.chdir('terraform')
        subprocess.run(['terraform', 'init'], check=True)
        subprocess.run(['terraform', 'apply', '-auto-approve', 
                       '-var=lambda_zip_path=../test-lambda.zip'], check=True)
        
        # Verify deployment
        # Note: In a real test, you would verify the Lambda function was created
        
        # Cleanup
        subprocess.run(['terraform', 'destroy', '-auto-approve',
                       '-var=lambda_zip_path=../test-lambda.zip'], check=True)
        os.chdir('..')
        
        # Clean up test files
        os.remove('test-lambda.zip')
        os.remove('test-lambda/lambda_function.py')
        os.rmdir('test-lambda')
