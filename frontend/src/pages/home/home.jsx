import "./home.css";
import { Link } from "react-router-dom"
import Share from "../../components/share/share";
import Profile from "../../components/profile/Profile";
import Stream from "../../components/stream/Stream";

const Home = () => {
    return (
      <div>
        <Profile/>
        <Share/>
        <Stream/>
      </div>
      // <div className="homeContainer">
      //   <Profile/>
      //   <div className="streamContainer">
      //   <Share/>
      //     <Stream/>
      //   </div>
      // </div>
    )
  }
  
  export default Home