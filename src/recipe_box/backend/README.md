# Recipe Box Backend API

A FastAPI backend for the Recipe Box application, packaged within the React frontend directory.

## Features

- **CRUD Operations**: Create, Read, Update, Delete recipes
- **Category Filtering**: Get recipes by category
- **Data Validation**: Pydantic models ensure data integrity
- **CORS Support**: Configured for frontend integration
- **File-based Storage**: Simple JSON storage (can be replaced with database)
- **Auto-generated Documentation**: Interactive API docs with Swagger UI

## API Endpoints

### Recipes
- `GET /recipes` - Get all recipes
- `GET /recipes/{recipe_id}` - Get specific recipe
- `POST /recipes` - Create new recipe
- `PUT /recipes/{recipe_id}` - Update recipe
- `DELETE /recipes/{recipe_id}` - Delete recipe

### Categories
- `GET /categories` - Get all unique categories
- `GET /recipes/category/{category}` - Get recipes by category

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server**:
   ```bash
   python main.py
   ```
   
   Or with uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## Data Models

### Recipe
```python
{
    "id": 1,
    "name": "Recipe Name",
    "ingredients": ["ingredient1", "ingredient2"],
    "instructions": ["step1", "step2"],
    "prep_time": 10,
    "cook_time": 20,
    "servings": 4,
    "category": "Italian",
    "created_at": "2023-12-01T10:00:00",
    "updated_at": "2023-12-01T10:00:00"
}
```

## Sample API Calls

### Create a Recipe
```bash
curl -X POST "http://localhost:8000/recipes" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pasta Carbonara",
    "ingredients": ["pasta", "eggs", "cheese"],
    "instructions": ["Boil pasta", "Mix ingredients"],
    "prep_time": 10,
    "cook_time": 15,
    "servings": 2,
    "category": "Italian"
  }'
```

### Get All Recipes
```bash
curl "http://localhost:8000/recipes"
```

### Get Recipe by ID
```bash
curl "http://localhost:8000/recipes/1"
```

## Frontend Integration

The backend is configured with CORS to work with the React frontend running on:
- http://localhost:3000
- http://127.0.0.1:3000

## Data Storage

Currently uses JSON file storage (`recipes.json`). For production, consider:
- PostgreSQL with SQLAlchemy
- MongoDB with motor
- Redis for caching
- Cloud databases (AWS RDS, Google Cloud SQL, etc.)

## Development

- **Hot Reload**: Use `uvicorn main:app --reload` for development
- **Environment Variables**: Add `.env` file for configuration
- **Logging**: Configure logging for production deployment
- **Testing**: Add pytest for API testing

## Project Structure

```
src/recipe_box/
├── backend/           # Python FastAPI backend
│   ├── main.py       # Main application
│   ├── requirements.txt
│   └── README.md
├── App.tsx           # React frontend
├── App.css           # Frontend styles
└── api.ts            # Frontend API service
``` 