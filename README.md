## KMS HACKATHON 2025

### AI-Powered Interview Preparation System

This is a FastAPI-based backend service that uses multi-agent AI system to analyze job descriptions and candidate CVs, then generates tailored interview questions.

---

## 🎯 Features

### AGENTS
- **JD Analyzer Agent**: Analyzes job descriptions and extracts key requirements
- **CV Analyzer Agent**: Analyzes candidate CV/resume and extracts qualifications
- **Skill Matcher Agent**: Matches candidate skills with job requirements
- **Question Generator Agent**: Generates personalized interview questions based on the analysis

---

## 🚀 Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.8+**
- **pip** (Python package manager)
- **AWS Account** with access to AWS Bedrock
- **AWS CLI** configured with appropriate credentials

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd kms-hackathon-be
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
# AWS Bedrock Configuration
MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
REGION_NAME=us-east-1

# AWS Credentials (if not using AWS CLI default profile)
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
```

> **Note**: Make sure your AWS IAM user/role has permissions to access AWS Bedrock services.

---

## 🏃 Running the Application

### Start the Server

```bash
python app.py
```

The server will start on `http://localhost:8000`

### Alternative: Using Uvicorn Directly

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The `--reload` flag enables auto-reload during development.

---

## 📡 API Endpoints

### 1. Health Check
- **Endpoint**: `GET /health`
- **Description**: Check if the service is running
- **Response**:
  ```json
  {
    "status": "healthy",
    "service": "interview-preparation-api",
    "version": "1.0.0"
  }
  ```

### 2. Prepare Interview
- **Endpoint**: `POST /prepare-interview`
- **Description**: Analyzes JD and CV, then generates interview questions
- **Request**:
  - Content-Type: `multipart/form-data`
  - Parameters:
    - `jd_text` (string): Job description text
    - `cv_file` (file): CV file (PDF or DOCX format)
- **Response**:
  ```json
  {
    "status": "completed",
    "execution_time": 12.34,
    "timestamp": "2025-10-13 12:34:56",
    "jd_analysis": { ... },
    "cv_analysis": { ... },
    "skill_matcher": { ... },
    "question_generator": { ... }
  }
  ```

---

## 🧪 Testing the API

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Prepare interview
curl -X POST http://localhost:8000/prepare-interview \
  -F "jd_text=Looking for a Senior Python Developer with FastAPI experience..." \
  -F "cv_file=@/path/to/cv.pdf"
```

### Using Postman or Thunder Client
1. Open Postman/Thunder Client
2. Create a new POST request to `http://localhost:8000/prepare-interview`
3. Select `Body` → `form-data`
4. Add fields:
   - `jd_text` (Text): Paste job description
   - `cv_file` (File): Upload CV (PDF or DOCX)
5. Send the request

### Using Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI interactive documentation.

---

## 📁 Project Structure

```
kms-hackathon-be/
├── agents/              # AI agent implementations
│   ├── jd_analyzer/
│   ├── cv_analyzer/
│   ├── skill_matcher/
│   └── question_generator/
├── conditions/          # Graph workflow conditions
├── models/              # Pydantic models
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

---

## 🔧 Development

### Adding New Dependencies

```bash
pip install <package-name>
pip freeze > requirements.txt
```

### Running in Development Mode

```bash
uvicorn app:app --reload --log-level debug
```

---

## 🐛 Troubleshooting

### Issue: AWS Credentials Error
**Solution**: Ensure AWS credentials are properly configured in `.env` or via AWS CLI:
```bash
aws configure
```

### Issue: Module Not Found
**Solution**: Make sure the virtual environment is activated and all dependencies are installed:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Port Already in Use
**Solution**: Change the port in `app.py` or kill the process using port 8000:
```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9
```

---

## 📝 Notes

- Supported CV formats: PDF, DOCX
- The system uses AWS Bedrock with Claude 3 Sonnet model
- CORS is enabled for all origins (configure for production)
- All file processing is done in-memory (no files saved to disk)

---

## 👥 Contributors

KMS Hackathon 2025 Team
