import React, { useState, useEffect } from 'react';
import './App.css';

// Utility function to generate random colors
const getRandomColor = (): string => {
  const colors = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
    '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
    '#F8C471', '#82E0AA', '#F1948A', '#85C1E9', '#D7BDE2'
  ];
  return colors[Math.floor(Math.random() * colors.length)];
};

const App: React.FC = () => {
  const [textColor, setTextColor] = useState<string>('#FF6B6B');
  const [consoleMessage, setConsoleMessage] = useState<string>('');

  // Generate new random color and log to console
  const changeColor = () => {
    const newColor = getRandomColor();
    setTextColor(newColor);
    const message = `Hello World! (Color: ${newColor})`;
    console.log(message);
    setConsoleMessage(message);
  };

  // Initial color and console log
  useEffect(() => {
    changeColor();
  }, []);

  return (
    <div className="App">
      <div className="container">
        <h1 
          className="hello-text"
          style={{ color: textColor }}
          onClick={changeColor}
        >
          Hello World!
        </h1>
        <p className="instructions">
          Click the text to change colors and see console output
        </p>
        {consoleMessage && (
          <div className="console-output">
            <p>Last console message:</p>
            <code>{consoleMessage}</code>
          </div>
        )}
      </div>
    </div>
  );
};

export default App; 