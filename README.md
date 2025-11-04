# FastAPI Application

Extract audio from video MP4 file

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

## Endpoints

- `GET /` - Root endpoint
- `POST /video/extract-audio` - Extract audio from video

## Project Structure

```
.
├── main.py          # Main FastAPI application
├── requirements.txt # Python dependencies
└── README.md
```
