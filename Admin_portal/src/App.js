import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Admin_Login from './frontend/pages/Admin_Login';
import Admin_Panel from './frontend/pages/Admin_Panel';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Admin_Login />} />
        <Route path="/dashboard" element={< Admin_Panel />} />
      </Routes>
    </Router>
  );
}

export default App