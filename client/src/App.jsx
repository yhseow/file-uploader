import React from 'react';
import './App.css'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import UploadFile from './components/UploadFile';
import UploadList from './components/UploadList';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Upload</Link>
            </li>
            <li>
              <Link to="/list">History</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<UploadFile />}></Route>
          <Route path="/list" element={<UploadList />}></Route>
        </Routes>
      </div>
    </Router>
  )
}

export default App
