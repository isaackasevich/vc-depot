#!/usr/bin/env python3
"""
Database initialization script for Recipe Box
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Initialize the database with tables and sample data"""
    
    # Database URL from environment variable
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://recipe_user:recipe_password@localhost:5432/recipe_box")
    
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            print(f"✅ Connected to PostgreSQL: {result.fetchone()[0]}")
        
        # Create tables
        print("📋 Creating database tables...")
        
        # Create recipes table
        create_recipes_table = """
        CREATE TABLE IF NOT EXISTS recipes (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            ingredients TEXT[] NOT NULL,
            instructions TEXT[] NOT NULL,
            prep_time INTEGER NOT NULL DEFAULT 0,
            cook_time INTEGER NOT NULL DEFAULT 0,
            servings INTEGER NOT NULL DEFAULT 1,
            category VARCHAR(100) NOT NULL DEFAULT 'Other',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        with engine.connect() as conn:
            conn.execute(text(create_recipes_table))
            conn.commit()
        
        print("✅ Recipes table created successfully")
        
        # Insert sample data
        print("📝 Inserting sample data...")
        
        sample_recipes = [
            {
                "name": "Spaghetti Carbonara",
                "ingredients": ["400g spaghetti", "200g pancetta", "4 large eggs", "100g Pecorino Romano cheese", "100g Parmigiano-Reggiano", "Black pepper", "Salt"],
                "instructions": [
                    "Bring a large pot of salted water to boil and cook spaghetti according to package directions",
                    "While pasta cooks, cut pancetta into small cubes and cook in a large skillet until crispy",
                    "In a bowl, whisk together eggs, grated cheeses, and black pepper",
                    "Drain pasta, reserving 1 cup of pasta water",
                    "Add hot pasta to the skillet with pancetta, remove from heat",
                    "Quickly stir in egg mixture, adding pasta water as needed to create a creamy sauce",
                    "Serve immediately with extra cheese and black pepper"
                ],
                "prep_time": 10,
                "cook_time": 15,
                "servings": 4,
                "category": "Italian"
            },
            {
                "name": "Chicken Tikka Masala",
                "ingredients": ["1kg chicken breast, cubed", "2 cups yogurt", "2 tbsp garam masala", "1 tbsp turmeric", "2 tbsp ginger-garlic paste", "2 onions, diced", "3 tomatoes, pureed", "1 cup heavy cream", "Fresh cilantro", "Basmati rice"],
                "instructions": [
                    "Marinate chicken in yogurt, garam masala, turmeric, and ginger-garlic paste for 2 hours",
                    "Grill or bake chicken until charred and cooked through",
                    "Sauté onions until golden brown",
                    "Add tomato puree and cook until thickened",
                    "Add grilled chicken and simmer for 10 minutes",
                    "Stir in heavy cream and simmer for 5 more minutes",
                    "Garnish with fresh cilantro and serve with basmati rice"
                ],
                "prep_time": 20,
                "cook_time": 30,
                "servings": 6,
                "category": "Indian"
            }
        ]
        
        insert_query = """
        INSERT INTO recipes (name, ingredients, instructions, prep_time, cook_time, servings, category)
        VALUES (:name, :ingredients, :instructions, :prep_time, :cook_time, :servings, :category)
        ON CONFLICT (id) DO NOTHING;
        """
        
        with engine.connect() as conn:
            for recipe in sample_recipes:
                conn.execute(text(insert_query), recipe)
            conn.commit()
        
        print("✅ Sample data inserted successfully")
        print("🎉 Database initialization complete!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database() 