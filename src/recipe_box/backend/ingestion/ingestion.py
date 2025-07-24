from abc import ABC, abstractmethod
from typing import Any, Dict
from sqlalchemy.orm import Session
import os

class RecipeIngestionBase(ABC):
    """
    Abstract base class for ingesting new recipes.
    Handles authentication, data retrieval, and database writing.
    """
    def __init__(self, db_session: Session):
        self.db = db_session
        self.authenticated = False

    def authenticate(self) -> bool:
        """
        Authenticate with an external system (placeholder).
        Returns True if authentication is successful.
        """
        # Placeholder for external authentication logic
        # Example: OAuth, API key, etc.
        # Set self.authenticated = True if successful
        self.authenticated = True  # Replace with real logic
        return self.authenticated

    @abstractmethod
    def get_recipe_data(self, **kwargs) -> Dict[str, Any]:
        """
        Abstract method to retrieve recipe data.
        Should return a dictionary with recipe fields.
        """
        pass

    def write_to_database(self, recipe_data: Dict[str, Any]):
        """
        Write the recipe data to the database.
        Assumes a SQLAlchemy Recipe model is available.
        """
        from models import Recipe  # Import here to avoid circular imports
        if not self.authenticated:
            raise PermissionError("Not authenticated. Call authenticate() first.")
        recipe = Recipe(**recipe_data)
        self.db.add(recipe)
        self.db.commit()
        self.db.refresh(recipe)
        return recipe

    def ingest(self, **kwargs):
        """
        Full ingestion pipeline: authenticate, get data, write to DB.
        """
        if not self.authenticate():
            raise PermissionError("Authentication failed.")
        recipe_data = self.get_recipe_data(**kwargs)
        return self.write_to_database(recipe_data)
