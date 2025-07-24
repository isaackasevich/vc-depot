#!/usr/bin/env python3
"""
Database initialization script for Recipe Box
"""

import os
import sys
import csv
import json
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = os.path.join(os.path.dirname(__file__), 'sample_recipes.csv')

def load_recipes_from_csv(csv_path):
    recipes = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Parse JSON arrays for ingredients and instructions
            row['ingredients'] = json.loads(row['ingredients'])
            row['instructions'] = json.loads(row['instructions'])
            row['prep_time'] = int(row['prep_time'])
            row['cook_time'] = int(row['cook_time'])
            row['servings'] = int(row['servings'])
            recipes.append(row)
    return recipes

def init_database():
    """Initialize the database with tables and sample data from CSV"""
    
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
        
        # Insert sample data from CSV
        print(f"📝 Inserting sample data from {CSV_PATH} ...")
        sample_recipes = load_recipes_from_csv(CSV_PATH)
        
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