import { useState } from "react";

import "./home.css";
import Share from "../../components/share/Share";
import Profile from "../../components/profile/Profile";
import Stream from "../../components/stream/Stream";

import Widgets from "../../components/widgets/Widgets";
import Post from "../../components/post/Post";
import NavBar from "../../components/navBar/NavBar";
import FollowRequest from "../../components/followRequests/followRequest";
import GitHubActivity from "../../components/github/Github";

const Home = () => {
  const [postsUpdated, setPostsUpdated] = useState(false);
  return (
    <div className="homeContainer">
      {/* <div className="navBarContainer">
        <NavBar/>
      </div> */}
      <div className="bodyContainer">
        <div className="profileContainer">
          <Profile/>
        </div>
        <div className="streamContainer">
          {/* <Share postsUpdated={postsUpdated} setPostsUpdated={setPostsUpdated}/>
          <Stream postsUpdated={postsUpdated}/> */}
          <GitHubActivity/>
        </div>
        <div className="widgetContainer">
           <Widgets/>
           <FollowRequest/>
        </div>
      </div>
    </div>
  )
}

export default Home