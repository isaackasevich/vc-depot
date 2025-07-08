import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import HelloWorldApp from './hello_world/App';
import RecipeBoxApp from './recipe_box/App';

const ProjectSelector: React.FC = () => {
  const [selectedProject, setSelectedProject] = useState<'hello_world' | 'recipe_box' | null>(null);

  if (selectedProject === 'hello_world') {
    return <HelloWorldApp />;
  }

  if (selectedProject === 'recipe_box') {
    return <RecipeBoxApp />;
  }

  return (
    <div className="project-selector">
      <div className="selector-container">
        <h1>🚀 VC Depot</h1>
        <p>Select a project to run:</p>
        <div className="project-buttons">
          <button 
            className="project-btn hello-world-btn"
            onClick={() => setSelectedProject('hello_world')}
          >
            <span className="project-icon">👋</span>
            <span className="project-title">Hello World</span>
            <span className="project-desc">Interactive color-changing hello world app</span>
          </button>
          <button 
            className="project-btn recipe-box-btn"
            onClick={() => setSelectedProject('recipe_box')}
          >
            <span className="project-icon">🍳</span>
            <span className="project-title">Recipe Box</span>
            <span className="project-desc">Recipe management application</span>
          </button>
        </div>
      </div>
    </div>
  );
};

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <ProjectSelector />
  </React.StrictMode>
); 