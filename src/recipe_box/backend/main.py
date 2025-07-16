from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime
import json
import os

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

# Simple file-based storage (you can replace with a real database later)
RECIPES_FILE = "recipes.json"

def load_recipes() -> List[Recipe]:
    """Load recipes from JSON file"""
    if os.path.exists(RECIPES_FILE):
        with open(RECIPES_FILE, 'r') as f:
            data = json.load(f)
            return [Recipe(**recipe) for recipe in data]
    return []

def save_recipes(recipes: List[Recipe]):
    """Save recipes to JSON file"""
    with open(RECIPES_FILE, 'w') as f:
        json.dump([recipe.dict() for recipe in recipes], f, indent=2)

def get_next_id(recipes: List[Recipe]) -> int:
    """Get next available ID"""
    if not recipes:
        return 1
    return max(recipe.id for recipe in recipes if recipe.id) + 1

# Initialize with sample data if no recipes exist
def initialize_sample_data():
    """Initialize with sample recipes if none exist"""
    recipes = load_recipes()
    if not recipes:
        sample_recipes = [
            Recipe(
                id=1,
                name="Spaghetti Carbonara",
                ingredients=[
                    "400g spaghetti",
                    "200g pancetta or guanciale",
                    "4 large eggs",
                    "100g Pecorino Romano cheese",
                    "100g Parmigiano-Reggiano",
                    "Black pepper",
                    "Salt"
                ],
                instructions=[
                    "Bring a large pot of salted water to boil and cook spaghetti according to package directions",
                    "While pasta cooks, cut pancetta into small cubes and cook in a large skillet until crispy",
                    "In a bowl, whisk together eggs, grated cheeses, and black pepper",
                    "Drain pasta, reserving 1 cup of pasta water",
                    "Add hot pasta to the skillet with pancetta, remove from heat",
                    "Quickly stir in egg mixture, adding pasta water as needed to create a creamy sauce",
                    "Serve immediately with extra cheese and black pepper"
                ],
                prep_time=10,
                cook_time=15,
                servings=4,
                category="Italian",
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            ),
            Recipe(
                id=2,
                name="Chicken Tikka Masala",
                ingredients=[
                    "1kg chicken breast, cubed",
                    "2 cups yogurt",
                    "2 tbsp garam masala",
                    "1 tbsp turmeric",
                    "2 tbsp ginger-garlic paste",
                    "2 onions, diced",
                    "3 tomatoes, pureed",
                    "1 cup heavy cream",
                    "Fresh cilantro",
                    "Basmati rice"
                ],
                instructions=[
                    "Marinate chicken in yogurt, garam masala, turmeric, and ginger-garlic paste for 2 hours",
                    "Grill or bake chicken until charred and cooked through",
                    "Sauté onions until golden brown",
                    "Add tomato puree and cook until thickened",
                    "Add grilled chicken and simmer for 10 minutes",
                    "Stir in heavy cream and simmer for 5 more minutes",
                    "Garnish with fresh cilantro and serve with basmati rice"
                ],
                prep_time=20,
                cook_time=30,
                servings=6,
                category="Indian",
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat()
            )
        ]
        save_recipes(sample_recipes)

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Recipe Box API is running!"}

@app.get("/recipes", response_model=List[Recipe])
async def get_recipes():
    """Get all recipes"""
    recipes = load_recipes()
    return recipes

@app.get("/recipes/{recipe_id}", response_model=Recipe)
async def get_recipe(recipe_id: int):
    """Get a specific recipe by ID"""
    recipes = load_recipes()
    recipe = next((r for r in recipes if r.id == recipe_id), None)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.post("/recipes", response_model=Recipe)
async def create_recipe(recipe_data: RecipeCreate):
    """Create a new recipe"""
    recipes = load_recipes()
    
    # Filter out empty ingredients and instructions
    filtered_ingredients = [ing for ing in recipe_data.ingredients if ing.strip()]
    filtered_instructions = [inst for inst in recipe_data.instructions if inst.strip()]
    
    if not filtered_ingredients or not filtered_instructions:
        raise HTTPException(status_code=400, detail="Ingredients and instructions cannot be empty")
    
    new_recipe = Recipe(
        id=get_next_id(recipes),
        name=recipe_data.name,
        ingredients=filtered_ingredients,
        instructions=filtered_instructions,
        prep_time=recipe_data.prep_time,
        cook_time=recipe_data.cook_time,
        servings=recipe_data.servings,
        category=recipe_data.category or "Other",
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    recipes.append(new_recipe)
    save_recipes(recipes)
    return new_recipe

@app.put("/recipes/{recipe_id}", response_model=Recipe)
async def update_recipe(recipe_id: int, recipe_data: RecipeUpdate):
    """Update an existing recipe"""
    recipes = load_recipes()
    recipe_index = next((i for i, r in enumerate(recipes) if r.id == recipe_id), None)
    
    if recipe_index is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    recipe = recipes[recipe_index]
    
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
        setattr(recipe, field, value)
    
    recipe.updated_at = datetime.now().isoformat()
    recipes[recipe_index] = recipe
    save_recipes(recipes)
    
    return recipe

@app.delete("/recipes/{recipe_id}")
async def delete_recipe(recipe_id: int):
    """Delete a recipe"""
    recipes = load_recipes()
    recipe = next((r for r in recipes if r.id == recipe_id), None)
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    recipes = [r for r in recipes if r.id != recipe_id]
    save_recipes(recipes)
    
    return {"message": "Recipe deleted successfully"}

@app.get("/recipes/category/{category}")
async def get_recipes_by_category(category: str):
    """Get recipes by category"""
    recipes = load_recipes()
    filtered_recipes = [r for r in recipes if r.category.lower() == category.lower()]
    return filtered_recipes

@app.get("/categories")
async def get_categories():
    """Get all unique categories"""
    recipes = load_recipes()
    categories = list(set(r.category for r in recipes))
    return {"categories": categories}

# Initialize sample data on startup
@app.on_event("startup")
async def startup_event():
    initialize_sample_data()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 