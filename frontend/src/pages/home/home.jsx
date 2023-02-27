import "./home.css"
import { Link } from "react-router-dom"
import Share from "../../components/share/share"
import Profile from "../../components/profile/Profile"

const Home = () => {
    return (
      <>
      <div className="homeContainer">
        <Profile/>
        <Share/>
      </div>
      </>
    )
  }
  
  export default Home