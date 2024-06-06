import React from 'react';
import './App.css';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import CVUpload from './components/CVuploads';
import CVList from './components/CVlist';
import Chatbot from './components/ChatBot';

function App() {
  return (
    <Router>
      <div className="App">
        <aside className="App-aside">
        <Link to="/">
            <button className="home-button">Home</button>
          </Link>
          <div />
          <Link to="/files">
            <button className="view-files-button">View Uploaded CV</button>
          </Link>
          <div />
          <Link to="/chatbot">
            <button className="chatbot-button">Chatbot</button>
          </Link>
        </aside>
        <div className="App-content">
          <header className="App-header">
            <Routes>
              <Route path="/" element={<CVUpload />} />
              <Route path="/files" element={<CVList />} />
              <Route path="/chatbot" element={<Chatbot />} />
            </Routes>
          </header>
        </div>
      </div>
    </Router>
  );
}

export default App;
