import React from 'react';
import './App.css';
import Login from "./pages/login/Login";
import Register from "./pages/register/Register";
import Home from './pages/home/Home';

import { createBrowserRouter, RouterProvider, Route} from "react-router-dom";

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
        <Home/>

    </div>
  );
  return <RouterProvider router = {router} />
}

export default App;
