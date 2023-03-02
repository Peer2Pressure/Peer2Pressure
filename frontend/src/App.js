import React from 'react';
import './App.css';
import Login from "./pages/login/Login";
import Register from "./pages/register/Register";
import Profile from './components/profile/Profile';
import Stream  from './components/stream/Stream';
import { createBrowserRouter, RouterProvider, Route} from "react-router-dom"
import Home from "./pages/home/home";

const router = createBrowserRouter([
  {
    // NOTE: this will need to go to home if a user is logged in
    path: "/",
    element: <Login/>
  },
  {
    path: "/home",
    element: <Home/>
  },
  {
    path: "/login",
    element: <Login/>
  },
  {
    path: "/register",
    element: <Register/>
  }
])

function App() {
  return (
    <div className="app">
      <Profile/>
        <Stream/>
       
        {/* <Home/> */}

    </div>
  );
  return <RouterProvider router = {router} />
}

export default App;
