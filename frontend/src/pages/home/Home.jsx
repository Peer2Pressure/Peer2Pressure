import { useState } from "react";
import * as React from 'react';
import "./home.css";
import Share from "../../components/share/Share";
import Profile from "../../components/profile/Profile";
import Stream from "../../components/stream/Stream";

import Widgets from "../../components/widgets/Widgets";
import Post from "../../components/post/Post";
import NavBar from "../../components/navBar/NavBar";
import FollowRequest from "../../components/followRequests/followRequest";
import Box from '@mui/material/Box';
import Tab from '@mui/material/Tab';
import Tabs from '@mui/material/Tabs';
import Notification from "../../components/notification/notification";
import GitHubActivityFeed from "../../components/github/Github";
import useGetAuthorData from "../../useGetAuthorData";
import useGetTokens from "../../useGetTokens";


const Home = () => {
  const [postsUpdated, setPostsUpdated] = useState(true);
  const [tabValue, setTabValue] = useState('1');

  const handleChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const {tokens, tokenError} = useGetTokens();
  const {authorData, authorID} = useGetAuthorData();
  const authorGitHubUsername = authorData ? authorData.github.replace(/\/$/, "").split("/").pop(): '';
  console.log("okay", authorGitHubUsername);

  if (!authorData || !authorID || !tokens) {
    return <div></div>;
  }

  return (
    <div className="homeContainer">
      {/* <div className="navBarContainer">
        <NavBar/>
      </div> */}
      <div className="bodyContainer">
        <div className="profileContainer">
          <Profile authorData={authorData} authorID={authorID} tokens={tokens}/>
          
        </div>
        <div className="streamContainer">
          <Share authorData={authorData} authorID={authorID} tokens={tokens}/>
          <br></br>
          <Box sx={{ "& .MuiTab-root": {borderBottom: 1, 
            borderColor: 'divider',
            fontWeight: 600,
            fontFamily: 'Montserrat, sans-serif;',
            color: "#2C4268" ,}, "& .Mui-selected": {
              color: "#007BBA",
            },
            }}>
            <Tabs value={tabValue} onChange={handleChange}>
              <Tab label="Regular Stream" value="1" />
              <Tab label="Direct Message" value="2" />
              <Tab label="GitHub Activity" value="3" />
            </Tabs>
          </Box>
          {tabValue === "1" && <Stream authorData={authorData} authorID={authorID} tokens={tokens} filterParam={true}/>}
          {tabValue === "2" && <Stream authorData={authorData} authorID={authorID} tokens={tokens} filterParam={false}/>}
          {tabValue === "3" && <GitHubActivityFeed
            username={authorGitHubUsername ? authorGitHubUsername : ''}
            // username={usea}
            limit={20}
          />}
        </div>
        <div className="widgetContainer">
           <Widgets authorData={authorData} authorID={authorID} tokens={tokens}/>
           <FollowRequest authorData={authorData} authorID={authorID} tokens={tokens}/>
           <Notification authorData={authorData} authorID={authorID} tokens={tokens}/>
        </div>
      </div>
    </div>
  )
}

export default Home