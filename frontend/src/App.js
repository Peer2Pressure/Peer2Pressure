import React from 'react';
import './App.css';
import Login from "./pages/login/Login";
import Register from "./pages/register/Register";
import Profile from './components/profile/Profile';
import Stream  from './components/stream/Stream';
import { BrowserRouter as Router, Route, Routes} from "react-router-dom";
import Home from "./pages/home/Home";
import ProfileSetting from './components/profileSetting/ProfileSetting';
import ProfilePage from './pages/profilePage/ProfilePage';

function App() {
  return (
    // <Router>
    //   <div className="app">
    //     <Routes>
    //       <Route path="/" element={<Home/>} />
    //       <Route path="/home" element={<Home/>} />
    //       {/* <Route path="/login" component={<Login/>} />
    //       <Route path="/register" component={<Register/>} /> */}
    //       <Route path="/home/settings" component={<ProfilePage/>} />
    //     </Routes>
    //   </div>
    // </Router>
    <ProfilePage/>
  );
}

export default App;
