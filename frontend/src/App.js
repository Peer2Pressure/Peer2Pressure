import React from 'react';
import './App.css';
import Login from "./pages/login/Login";
import Register from "./pages/register/Register";
import Profile from './components/profile/Profile';
import Stream  from './components/stream/Stream';
import { BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Home from "./pages/home/Home";
import ProfilePage from './pages/profilePage/ProfilePage';

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          <Route exact path="/" element={<Home/>} />
          <Route path="/profilepage" element={<ProfilePage/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
