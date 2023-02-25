import Login from "./pages/login/Login";
import Register from "./pages/register/Register";

import { createBrowserRouter, RouterProvider, Route} from "react-router-dom"

const router = createBrowserRouter([
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
