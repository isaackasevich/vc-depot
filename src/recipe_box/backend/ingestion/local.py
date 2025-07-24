import os
import csv
import json
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from .ingestion import RecipeIngestionBase

class LocalCSVIngestion(RecipeIngestionBase):
    """
    Ingest recipes from a local CSV file (e.g., sample_recipes.csv).
    """
    def __init__(self, db_session: Session, csv_path: str):
        super().__init__(db_session)
        self.csv_path = csv_path

    def get_recipe_data(self, row_index: int = 0, **kwargs) -> Dict[str, Any]:
        """
        Retrieve a single recipe from the CSV file by row index (default: first row).
        Returns a dictionary with recipe fields.
        """
        recipes = self._load_all_recipes_from_csv()
        if not recipes:
            raise ValueError(f"No recipes found in CSV: {self.csv_path}")
        if row_index < 0 or row_index >= len(recipes):
            raise IndexError(f"Row index {row_index} out of range for CSV with {len(recipes)} recipes.")
        return recipes[row_index]

    def _load_all_recipes_from_csv(self) -> List[Dict[str, Any]]:
        recipes = []
        with open(self.csv_path, newline='', encoding='utf-8') as csvfile:
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

    def ingest_all(self) -> List[Any]:
        """
        Ingest all recipes from the CSV file into the database.
        Returns a list of created Recipe objects.
        """
        if not self.authenticate():
            raise PermissionError("Authentication failed.")
        recipes = self._load_all_recipes_from_csv()
        created = []
        for recipe_data in recipes:
            created.append(self.write_to_database(recipe_data))
        return created
