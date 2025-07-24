from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
import os
import json
from sqlalchemy.orm import Session
from database import get_db, create_tables
from models import Recipe as DBRecipe

# Pydantic models (equivalent to TypeScript interfaces)
class Recipe(BaseModel):
    id: Optional[int] = None
    name: str
    ingredients: List[str]
    instructions: List[str]
    prep_time: int
    cook_time: int
    servings: int
    category: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class RecipeCreate(BaseModel):
    name: str
    ingredients: List[str]
    instructions: List[str]
    prep_time: int
    cook_time: int
    servings: int
    category: str

class RecipeUpdate(BaseModel):
    name: Optional[str] = None
    ingredients: Optional[List[str]] = None
    instructions: Optional[List[str]] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: Optional[int] = None
    category: Optional[str] = None

# Initialize FastAPI app
app = FastAPI(
    title="Recipe Box API",
    description="A backend API for managing recipes",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database helper functions
def recipe_to_dict(db_recipe) -> dict:
    """Convert database recipe to dictionary"""
    return {
        "id": db_recipe.id,
        "name": db_recipe.name,
        "ingredients": db_recipe.ingredients,
        "instructions": db_recipe.instructions,
        "prep_time": db_recipe.prep_time,
        "cook_time": db_recipe.cook_time,
        "servings": db_recipe.servings,
        "category": db_recipe.category,
        "created_at": db_recipe.created_at.isoformat() if db_recipe.created_at else None,
        "updated_at": db_recipe.updated_at.isoformat() if db_recipe.updated_at else None
    }

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Recipe Box API is running!"}

@app.get("/recipes", response_model=List[Recipe])
async def get_recipes(db: Session = Depends(get_db)):
    """Get all recipes"""
    db_recipes = db.query(DBRecipe).all()
    return [recipe_to_dict(recipe) for recipe in db_recipes]

@app.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Get a specific recipe by ID"""
    db_recipe = db.query(DBRecipe).filter(DBRecipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe_to_dict(db_recipe)

@app.post("/recipes", response_model=Recipe)
async def create_recipe(recipe_data: RecipeCreate, db: Session = Depends(get_db)):
    """Create a new recipe"""
    # Filter out empty ingredients and instructions
    filtered_ingredients = [ing for ing in recipe_data.ingredients if ing.strip()]
    filtered_instructions = [inst for inst in recipe_data.instructions if inst.strip()]
    
    if not filtered_ingredients or not filtered_instructions:
        raise HTTPException(status_code=400, detail="Ingredients and instructions cannot be empty")
    
    db_recipe = DBRecipe(
        name=recipe_data.name,
        ingredients=filtered_ingredients,
        instructions=filtered_instructions,
        prep_time=recipe_data.prep_time,
        cook_time=recipe_data.cook_time,
        servings=recipe_data.servings,
        category=recipe_data.category or "Other"
    )
    
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return recipe_to_dict(db_recipe)

@app.put("/recipes/{recipe_id}", response_model=Recipe)
async def update_recipe(recipe_id: int, recipe_data: RecipeUpdate, db: Session = Depends(get_db)):
    """Update an existing recipe"""
    db_recipe = db.query(DBRecipe).filter(DBRecipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Update only provided fields
    update_data = recipe_data.dict(exclude_unset=True)
    
    # Filter out empty ingredients and instructions if provided
    if "ingredients" in update_data:
        update_data["ingredients"] = [ing for ing in update_data["ingredients"] if ing.strip()]
        if not update_data["ingredients"]:
            raise HTTPException(status_code=400, detail="Ingredients cannot be empty")
    
    if "instructions" in update_data:
        update_data["instructions"] = [inst for inst in update_data["instructions"] if inst.strip()]
        if not update_data["instructions"]:
            raise HTTPException(status_code=400, detail="Instructions cannot be empty")
    
    # Update the recipe
    for field, value in update_data.items():
        setattr(db_recipe, field, value)
    
    db.commit()
    db.refresh(db_recipe)
    return recipe_to_dict(db_recipe)

@app.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Delete a recipe"""
    db_recipe = db.query(DBRecipe).filter(DBRecipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    db.delete(db_recipe)
    db.commit()
    
    return {"message": "Recipe deleted successfully"}

@app.get("/recipes/category/{category}")
async def get_recipes_by_category(category: str, db: Session = Depends(get_db)):
    """Get recipes by category"""
    db_recipes = db.query(DBRecipe).filter(DBRecipe.category.ilike(f"%{category}%")).all()
    return [recipe_to_dict(recipe) for recipe in db_recipes]

@app.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get all unique categories"""
    categories = db.query(DBRecipe.category).distinct().all()
    return {"categories": [cat[0] for cat in categories]}

# Initialize database and sample data on startup
@app.on_event("startup")
async def startup_event():
    # Create tables if they don't exist
    create_tables()
    print("✅ Database tables created")
    
    # Initialize sample data using the ingestion system
    try:
        from ingestion.local import LocalCSVIngestion
        from database import SessionLocal
        
        # Check if we have sample data
        db = SessionLocal()
        recipe_count = db.query(DBRecipe).count()
        
        if recipe_count == 0:
            print("📝 Initializing sample data from CSV...")
            csv_path = "sample_recipes.csv"
            if os.path.exists(csv_path):
                ingestion = LocalCSVIngestion(db, csv_path)
                ingestion.ingest_all()
                print("✅ Sample data loaded from CSV")
            else:
                print("⚠️ CSV file not found, skipping sample data")
        else:
            print(f"✅ Database has {recipe_count} recipes")
        
        db.close()
    except Exception as e:
        print(f"⚠️ Could not initialize sample data: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 