import Login from "./pages/login/Login";
import Register from "./pages/register/Register";

import { createBrowserRouter, RouterProvider, Route} from "react-router-dom"
import Home from "./pages/home/home";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Home/>
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
  return <RouterProvider router = {router} />
}

export default App;
