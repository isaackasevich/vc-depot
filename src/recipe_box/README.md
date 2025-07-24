# Recipe Box Application

A full-stack recipe management application with React frontend and Python FastAPI backend.

## Project Structure

```
src/recipe_box/
├── frontend/              # React frontend application
│   ├── App.tsx           # Main React component
│   ├── App.css           # Frontend styles
│   └── api.ts            # API service layer
├── backend/              # Python FastAPI backend
│   ├── main.py           # FastAPI application
│   ├── requirements.txt  # Python dependencies
│   ├── package.json      # Backend scripts
│   └── README.md         # Backend documentation
├── index.tsx             # Entry point for the application
└── README.md             # This file
```

## Quick Start

### 1. Start the Backend
```bash
cd src/recipe_box/backend
pip install -r requirements.txt
python main.py
```
Backend will be available at: http://localhost:8000

### 2. Start the Frontend
```bash
# From the project root
npm install
npm start
```
Frontend will be available at: http://localhost:3000

### 3. Access the Application
- Navigate to http://localhost:3000
- Select "Recipe Box" from the project selector
- Start managing your recipes!

## Features

### Frontend (React)
- Modern, responsive UI with glassmorphism design
- Real-time recipe management
- Form validation and error handling
- Loading states and user feedback

### Backend (FastAPI)
- RESTful API with full CRUD operations
- Data validation with Pydantic models
- CORS support for frontend integration
- File-based JSON storage (easily replaceable with database)
- Auto-generated API documentation

## API Endpoints

- `GET /recipes` - Get all recipes
- `GET /recipes/{id}` - Get specific recipe
- `POST /recipes` - Create new recipe
- `PUT /recipes/{id}` - Update recipe
- `DELETE /recipes/{id}` - Delete recipe
- `GET /categories` - Get all categories
- `GET /recipes/category/{category}` - Filter by category

## Development

### Backend Development
```bash
cd src/recipe_box/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
The frontend will automatically reload when you make changes.

### API Documentation
Visit http://localhost:8000/docs for interactive API documentation.

## Data Storage

Currently uses JSON file storage (`recipes.json`). For production, consider:
- PostgreSQL with SQLAlchemy
- MongoDB with motor
- Redis for caching
- Cloud databases (AWS RDS, Google Cloud SQL, etc.)

## Deployment

### Backend Deployment
- Deploy to Vercel, Railway, or any Python hosting platform
- Update CORS origins in `main.py` for production domains

### Frontend Deployment
- Build with `npm run build`
- Deploy to Vercel, Netlify, or any static hosting platform
- Update API base URL in `api.ts` for production backend

## Contributing

1. Make changes in the appropriate directory (`frontend/` or `backend/`)
2. Test both frontend and backend functionality
3. Update documentation as needed 