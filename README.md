# VC Depot

A multi-project React TypeScript application showcasing different projects in a single codebase.

## Project Structure

```
src/
├── hello_world/          # Interactive Hello World application
│   ├── App.tsx          # Main Hello World component
│   ├── App.css          # Hello World styles
│   └── index.tsx        # Hello World entry point
├── recipe_box/          # Recipe management application
│   ├── frontend/        # React frontend
│   │   ├── App.tsx      # Main Recipe Box component
│   │   ├── App.css      # Recipe Box styles
│   │   └── api.ts       # Frontend API service
│   ├── backend/         # Python FastAPI backend
│   │   ├── main.py      # Backend application
│   │   ├── requirements.txt
│   │   ├── package.json
│   │   └── README.md
│   ├── index.tsx        # Recipe Box entry point
│   └── README.md        # Recipe Box documentation
├── index.tsx            # Main application with project selector
├── index.css            # Global styles and project selector styles
└── ...
```

## Projects

### 👋 Hello World
An interactive application that displays "Hello World!" with clickable text that changes colors randomly. Features:
- Color-changing text on click
- Console logging functionality
- Modern glassmorphism UI design
- Responsive design

### 🍳 Recipe Box
A comprehensive recipe management application with the following features:
- View existing recipes in a card-based grid
- Add new recipes with detailed information
- Recipe details view with ingredients and instructions
- Categorization and metadata (prep time, cook time, servings)
- Modern, responsive UI with beautiful gradients

## Getting Started

### Frontend (React)

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Open [http://localhost:3000](http://localhost:3000) to view the project selector

4. Choose a project to run from the main interface

### Backend (Python FastAPI)

The Recipe Box now includes a Python backend API packaged within the frontend directory. To run it:

1. Navigate to the recipe box backend directory:
   ```bash
   cd src/recipe_box/backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```bash
   python main.py
   ```
   
   Or for development with auto-reload:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. The API will be available at:
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs

### Full Stack Setup

To run both frontend and backend:

1. **Terminal 1** - Start the backend:
   ```bash
   cd src/recipe_box/backend
   pip install -r requirements.txt
   python main.py
   ```

2. **Terminal 2** - Start the frontend:
   ```bash
   npm install
   npm start
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

## Technologies Used

- React 18
- TypeScript
- CSS3 with modern features (Grid, Flexbox, CSS Variables)
- Create React App

## Features

- **Multi-project Architecture**: Clean separation of different applications
- **Project Selector**: Beautiful interface to choose between projects
- **Modern UI**: Glassmorphism design with gradients and animations
- **Responsive Design**: Works on desktop and mobile devices
- **TypeScript**: Full type safety throughout the application
