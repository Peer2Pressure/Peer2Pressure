import "./navBar.css"

import React from 'react'
import { Button } from "@mui/material"

export default function NavBar() {
  return (
    <div class="navBarContainer">
        <div className="buttonContainer">
            <Button>Home</Button>
            <Button>Logout</Button>
        </div>
        
    </div>
  )
}
