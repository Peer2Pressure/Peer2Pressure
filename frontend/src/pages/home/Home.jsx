import "./home.css";
import Share from "../../components/share/Share";
import Profile from "../../components/profile/Profile";
import Stream from "../../components/stream/Stream";
import Widgets from "../../components/widgets/Widgets";
const Home = () => {
    return (
      // <div>
      //   <Profile/>
      //   <Share/>
      //   <Stream/>
      // </div>
      <div className="homeContainer">
        <Profile/>
        <div className="streamContainer">
          <Share/>
          <Stream/>
        </div>
        <Widgets/>
      </div>
    )
  }
  
  export default Home