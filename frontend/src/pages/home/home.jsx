import "./home.css";
import { Link } from "react-router-dom"
import Share from "../../components/share/Share";
import Profile from "../../components/profile/Profile";
import Stream from "../../components/stream/Stream";

const Home = () => {
    return (
      <>
      <div className="homeContainer">
        <div className="profileContainer">
          <Profile/>
        </div>
        <div className="streamContainer">
          <Share/>
          <Stream/>
        </div>
      </div>
      </>
    )
  }
  
  export default Home