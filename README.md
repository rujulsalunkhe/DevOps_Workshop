# DevOps CI/CD Pipeline Project

A complete end-to-end DevOps pipeline demonstrating CI/CD practices with LocalStack, GitHub Actions, Terraform, and Flask.

## 🚀 Features

### Core Requirements

- ✅ LocalStack (AWS simulation) running in Docker
- ✅ Self-hosted GitHub Actions runner
- ✅ Terraform Infrastructure as Code
- ✅ Flask REST API with multiple endpoints
- ✅ Complete CI/CD pipeline
- ✅ Automated testing and deployment

### Enhanced Features

- 🗄️ **SQLite Database Integration** - User management with persistence
- 📚 **API Documentation** - Swagger/OpenAPI specification
- 📊 **Logging & Monitoring** - Structured logging with different levels
- ✅ **Data Validation** - Input validation and error handling
- 🏥 **Health Checks** - Detailed health metrics and status
- ⚙️ **Environment Configuration** - Configurable settings
- 📦 **API Versioning** - Versioned endpoints for better management
- 🔒 **Security Headers** - Basic security implementations
- 🧪 **Testing Coverage** - Comprehensive unit and integration tests

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.9+
- Git
- Terraform
- GitHub account

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.9+
- Git
- Terraform
- GitHub account

## 🛠️ Setup Instructions

### 1. Clone Repository

git clone
cd devops-pipeline-project

### 2. Environment Setup

Copy environment file
cp .env.example .env
Create Python virtual environment
python3 -m venv venvsource venv/bin/activate # On Windows: venv\Scripts\activate
Install dependencies
pip install -r requirements.txt

### 3. LocalStack Setup

Start LocalStack
docker-compose up -d localstack
Verify LocalStack is running
curl http://localhost:4566/\_localstack/health

### 4. Self-Hosted Runner Setup

Download and configure GitHub Actions runner
Follow GitHub’s official documentation for your OS:
https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners
For Linux/macOS:
mkdir actions-runner && cd actions-runnercurl -o actions-runner-linux-x64-2.311.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gztar xzf ./actions-runner-linux-x64-2.311.0.tar.gz
Configure (replace with your repo URL and token)
./config.sh –url https://github.com/YOUR_USERNAME/YOUR_REPO –token YOUR_TOKEN
Start the runner
./run.sh

### 5. Test Local Application

Run Flask app locally
python app.py
Test endpoints
curl http://localhost:5000/curl
http://localhost:5000/healthcurl
http://localhost:5000/api/v1/users

### 6. Deploy with Terraform

cd terraform
terraform init
terraform plan
terraform apply

## 📡 API Endpoints

### Core Endpoints

- `GET /` - Welcome message with API information
- `GET /health` - Health check with detailed metrics
- `GET /api/v1/users` - Get all users
- `POST /api/v1/users` - Create new user
- `GET /api/v1/users/{id}` - Get user by ID
- `GET /api/v1/info` - Application metadata
- `GET /api/v1/docs` - API documentation

### Example Requests

Create user
curl -X POST http://localhost:5000/api/v1/users
-H “Content-Type: application/json”
-d ‘{“name”: “John Doe”, “email”: “john@example.com”}’
Get users
curl http://localhost:5000/api/v1/users
Health check
curl http://localhost:5000/health

## 🧪 Running Tests

Unit tests
pytest tests/test_app.py -v
Integration tests
pytest tests/test_integration.py -v
With coverage
pytest tests/ –cov=app –cov-report=html

## 🔄 CI/CD Pipeline

The pipeline triggers on push to main branch:

1. **Test Phase**

   - Checkout code
   - Setup Python environment
   - Install dependencies
   - Run unit tests with coverage
   - Code quality checks

2. **Deploy Phase**
   - Start LocalStack
   - Package Lambda function
   - Deploy infrastructure with Terraform
   - Test deployed endpoints

## 📁 Project Structure

devops-pipeline-project/
├── .github/workflows/deploy.yml # CI/CD pipeline
├── terraform/ # Infrastructure as Code
│ ├── main.tf
│ ├── variables.tf
│ └── outputs.tf
├── tests/ # Test files
│ ├── test_app.py
│ └── test_integration.py
├── app/ # Application modules
│ ├── init.py
│ ├── models.py
│ ├── config.py
│ └── utils.py
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── docker-compose.yml # LocalStack configuration
├── Dockerfile # Container configuration
├── .gitignore # Git ignore rules
├── .env.example # Environment template
└── README.md # This file

## 🐛 Troubleshooting

### Common Issues

**LocalStack Connection Issues**

Check if LocalStack is running
docker ps | grep localstack

Check LocalStack logs
docker logs localstack-devops

Restart LocalStack
docker-compose restart localstack

**Python Path Issues**

Ensure virtual environment is activated
source venv/bin/activate

Check Python path
echo $PYTHONPATH

**Terraform Issues**

Reset Terraform state
cd terraform
rm -rf .terraform terraform.tfstate\*
terraform init

**GitHub Runner Issues**

Check runner status
./run.sh –check

Reconfigure runner
./config.sh remove
./config.sh –url –token

## 📚 Learning Resources

- [LocalStack Documentation](https://docs.localstack.cloud/)
- [GitHub Actions Self-Hosted Runners](https://docs.github.com/en/actions/hosting-your-own-runners)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
