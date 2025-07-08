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
│   ├── App.tsx          # Main Recipe Box component
│   ├── App.css          # Recipe Box styles
│   └── index.tsx        # Recipe Box entry point
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
