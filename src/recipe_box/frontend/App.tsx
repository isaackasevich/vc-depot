import React, { useState, useEffect } from 'react';
import './App.css';
import { recipeAPI, Recipe, RecipeCreate } from './api';

const App: React.FC = () => {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newRecipe, setNewRecipe] = useState<Partial<Recipe>>({
    name: '',
    ingredients: [''],
    instructions: [''],
    prep_time: 0,
    cook_time: 0,
    servings: 1,
    category: ''
  });

  // Load recipes from API on component mount
  useEffect(() => {
    const loadRecipes = async () => {
      try {
        setLoading(true);
        const data = await recipeAPI.getRecipes();
        setRecipes(data);
        setError(null);
      } catch (err) {
        setError('Failed to load recipes. Make sure the backend is running on http://localhost:8000');
        console.error('Error loading recipes:', err);
      } finally {
        setLoading(false);
      }
    };

    loadRecipes();
  }, []);

  const addIngredient = () => {
    setNewRecipe(prev => ({
      ...prev,
      ingredients: [...(prev.ingredients || []), '']
    }));
  };

  const addInstruction = () => {
    setNewRecipe(prev => ({
      ...prev,
      instructions: [...(prev.instructions || []), '']
    }));
  };

  const updateIngredient = (index: number, value: string) => {
    setNewRecipe(prev => ({
      ...prev,
      ingredients: prev.ingredients?.map((ing, i) => i === index ? value : ing)
    }));
  };

  const updateInstruction = (index: number, value: string) => {
    setNewRecipe(prev => ({
      ...prev,
      instructions: prev.instructions?.map((inst, i) => i === index ? value : inst)
    }));
  };

  const saveRecipe = async () => {
    if (newRecipe.name && newRecipe.ingredients && newRecipe.instructions) {
      try {
        const recipeData: RecipeCreate = {
          name: newRecipe.name,
          ingredients: newRecipe.ingredients.filter(ing => ing.trim() !== ''),
          instructions: newRecipe.instructions.filter(inst => inst.trim() !== ''),
          prep_time: newRecipe.prep_time || 0,
          cook_time: newRecipe.cook_time || 0,
          servings: newRecipe.servings || 1,
          category: newRecipe.category || 'Other'
        };
        
        const savedRecipe = await recipeAPI.createRecipe(recipeData);
        setRecipes(prev => [...prev, savedRecipe]);
        setShowAddForm(false);
        setNewRecipe({
          name: '',
          ingredients: [''],
          instructions: [''],
          prep_time: 0,
          cook_time: 0,
          servings: 1,
          category: ''
        });
      } catch (err) {
        setError('Failed to save recipe. Please try again.');
        console.error('Error saving recipe:', err);
      }
    }
  };

  return (
    <div className="App">
      <header className="header">
        <h1>🍳 Recipe Box</h1>
        <button 
          className="add-recipe-btn"
          onClick={() => setShowAddForm(true)}
        >
          + Add Recipe
        </button>
      </header>

      <div className="container">
        {error && (
          <div className="error-message">
            <p>{error}</p>
            <button onClick={() => setError(null)}>Dismiss</button>
          </div>
        )}
        
        {loading ? (
          <div className="loading">
            <p>Loading recipes...</p>
          </div>
        ) : showAddForm ? (
          <div className="add-recipe-form">
            <h2>Add New Recipe</h2>
            <div className="form-group">
              <label>Recipe Name:</label>
              <input
                type="text"
                value={newRecipe.name}
                onChange={(e) => setNewRecipe(prev => ({ ...prev, name: e.target.value }))}
                placeholder="Enter recipe name"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Prep Time (min):</label>
                <input
                  type="number"
                  value={newRecipe.prep_time}
                  onChange={(e) => setNewRecipe(prev => ({ ...prev, prep_time: parseInt(e.target.value) || 0 }))}
                />
              </div>
              <div className="form-group">
                <label>Cook Time (min):</label>
                <input
                  type="number"
                  value={newRecipe.cook_time}
                  onChange={(e) => setNewRecipe(prev => ({ ...prev, cook_time: parseInt(e.target.value) || 0 }))}
                />
              </div>
              <div className="form-group">
                <label>Servings:</label>
                <input
                  type="number"
                  value={newRecipe.servings}
                  onChange={(e) => setNewRecipe(prev => ({ ...prev, servings: parseInt(e.target.value) || 1 }))}
                />
              </div>
            </div>

            <div className="form-group">
              <label>Category:</label>
              <input
                type="text"
                value={newRecipe.category}
                onChange={(e) => setNewRecipe(prev => ({ ...prev, category: e.target.value }))}
                placeholder="e.g., Italian, Indian, Mexican"
              />
            </div>

            <div className="form-group">
              <label>Ingredients:</label>
              {newRecipe.ingredients?.map((ingredient, index) => (
                <input
                  key={index}
                  type="text"
                  value={ingredient}
                  onChange={(e) => updateIngredient(index, e.target.value)}
                  placeholder={`Ingredient ${index + 1}`}
                />
              ))}
              <button type="button" onClick={addIngredient} className="add-btn">
                + Add Ingredient
              </button>
            </div>

            <div className="form-group">
              <label>Instructions:</label>
              {newRecipe.instructions?.map((instruction, index) => (
                <textarea
                  key={index}
                  value={instruction}
                  onChange={(e) => updateInstruction(index, e.target.value)}
                  placeholder={`Step ${index + 1}`}
                  rows={2}
                />
              ))}
              <button type="button" onClick={addInstruction} className="add-btn">
                + Add Step
              </button>
            </div>

            <div className="form-actions">
              <button onClick={saveRecipe} className="save-btn">Save Recipe</button>
              <button onClick={() => setShowAddForm(false)} className="cancel-btn">Cancel</button>
            </div>
          </div>
        ) : selectedRecipe ? (
          <div className="recipe-detail">
            <button onClick={() => setSelectedRecipe(null)} className="back-btn">
              ← Back to Recipes
            </button>
            <div className="recipe-header">
              <h2>{selectedRecipe.name}</h2>
              <div className="recipe-meta">
                <span>⏱️ Prep: {selectedRecipe.prep_time}min</span>
                <span>🔥 Cook: {selectedRecipe.cook_time}min</span>
                <span>👥 Serves: {selectedRecipe.servings}</span>
                <span>🏷️ {selectedRecipe.category}</span>
              </div>
            </div>

            <div className="recipe-content">
              <div className="ingredients-section">
                <h3>Ingredients</h3>
                <ul>
                  {selectedRecipe.ingredients.map((ingredient, index) => (
                    <li key={index}>{ingredient}</li>
                  ))}
                </ul>
              </div>

              <div className="instructions-section">
                <h3>Instructions</h3>
                <ol>
                  {selectedRecipe.instructions.map((instruction, index) => (
                    <li key={index}>{instruction}</li>
                  ))}
                </ol>
              </div>
            </div>
          </div>
        ) : (
          <div className="recipes-grid">
            {recipes.map(recipe => (
              <div 
                key={recipe.id} 
                className="recipe-card"
                onClick={() => setSelectedRecipe(recipe)}
              >
                <h3>{recipe.name}</h3>
                <div className="recipe-card-meta">
                  <span>⏱️ {recipe.prep_time + recipe.cook_time}min</span>
                  <span>👥 {recipe.servings} servings</span>
                  <span>🏷️ {recipe.category}</span>
                </div>
                <p className="recipe-preview">
                  {recipe.ingredients.slice(0, 3).join(', ')}
                  {recipe.ingredients.length > 3 && '...'}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default App; 