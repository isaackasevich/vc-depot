import React, { useState } from 'react';
import './App.css';

interface Recipe {
  id: number;
  name: string;
  ingredients: string[];
  instructions: string[];
  prepTime: number;
  cookTime: number;
  servings: number;
  category: string;
}

const App: React.FC = () => {
  const [recipes, setRecipes] = useState<Recipe[]>([
    {
      id: 1,
      name: "Spaghetti Carbonara",
      ingredients: [
        "400g spaghetti",
        "200g pancetta or guanciale",
        "4 large eggs",
        "100g Pecorino Romano cheese",
        "100g Parmigiano-Reggiano",
        "Black pepper",
        "Salt"
      ],
      instructions: [
        "Bring a large pot of salted water to boil and cook spaghetti according to package directions",
        "While pasta cooks, cut pancetta into small cubes and cook in a large skillet until crispy",
        "In a bowl, whisk together eggs, grated cheeses, and black pepper",
        "Drain pasta, reserving 1 cup of pasta water",
        "Add hot pasta to the skillet with pancetta, remove from heat",
        "Quickly stir in egg mixture, adding pasta water as needed to create a creamy sauce",
        "Serve immediately with extra cheese and black pepper"
      ],
      prepTime: 10,
      cookTime: 15,
      servings: 4,
      category: "Italian"
    },
    {
      id: 2,
      name: "Chicken Tikka Masala",
      ingredients: [
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
      instructions: [
        "Marinate chicken in yogurt, garam masala, turmeric, and ginger-garlic paste for 2 hours",
        "Grill or bake chicken until charred and cooked through",
        "Sauté onions until golden brown",
        "Add tomato puree and cook until thickened",
        "Add grilled chicken and simmer for 10 minutes",
        "Stir in heavy cream and simmer for 5 more minutes",
        "Garnish with fresh cilantro and serve with basmati rice"
      ],
      prepTime: 20,
      cookTime: 30,
      servings: 6,
      category: "Indian"
    }
  ]);

  const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newRecipe, setNewRecipe] = useState<Partial<Recipe>>({
    name: '',
    ingredients: [''],
    instructions: [''],
    prepTime: 0,
    cookTime: 0,
    servings: 1,
    category: ''
  });

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

  const saveRecipe = () => {
    if (newRecipe.name && newRecipe.ingredients && newRecipe.instructions) {
      const recipe: Recipe = {
        id: Date.now(),
        name: newRecipe.name,
        ingredients: newRecipe.ingredients.filter(ing => ing.trim() !== ''),
        instructions: newRecipe.instructions.filter(inst => inst.trim() !== ''),
        prepTime: newRecipe.prepTime || 0,
        cookTime: newRecipe.cookTime || 0,
        servings: newRecipe.servings || 1,
        category: newRecipe.category || 'Other'
      };
      setRecipes(prev => [...prev, recipe]);
      setShowAddForm(false);
      setNewRecipe({
        name: '',
        ingredients: [''],
        instructions: [''],
        prepTime: 0,
        cookTime: 0,
        servings: 1,
        category: ''
      });
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
        {showAddForm ? (
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
                  value={newRecipe.prepTime}
                  onChange={(e) => setNewRecipe(prev => ({ ...prev, prepTime: parseInt(e.target.value) || 0 }))}
                />
              </div>
              <div className="form-group">
                <label>Cook Time (min):</label>
                <input
                  type="number"
                  value={newRecipe.cookTime}
                  onChange={(e) => setNewRecipe(prev => ({ ...prev, cookTime: parseInt(e.target.value) || 0 }))}
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
                <span>⏱️ Prep: {selectedRecipe.prepTime}min</span>
                <span>🔥 Cook: {selectedRecipe.cookTime}min</span>
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
                  <span>⏱️ {recipe.prepTime + recipe.cookTime}min</span>
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