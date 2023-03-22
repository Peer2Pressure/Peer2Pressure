import "./home.css";
import Share from "../../components/share/Share";
import Profile from "../../components/profile/Profile";
import Stream from "../../components/stream/Stream";
import Post from "../../components/post/Post";

import Post from "../../components/post/Post";

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
          <Post/>
        </div>
      </div>
    )
  }
  
  export default Home