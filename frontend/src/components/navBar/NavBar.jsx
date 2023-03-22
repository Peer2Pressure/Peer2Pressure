import "./navBar.css"
import HomeIcon from '@mui/icons-material/Home';
import LogoutIcon from '@mui/icons-material/Logout';


import React from 'react'
import { Button } from "@mui/material"

export default function NavBar() {
  return (
    <div class="navBarContainer">
        <div className="buttonContainer">
            <Button startIcon={<HomeIcon/>}>
              Home
            </Button>
            <Button endIcon={<LogoutIcon/>}>
              Logout
            </Button>
        </div>
        
    </div>
  )
}
