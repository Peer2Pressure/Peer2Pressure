import "./profile.css"
import useFetch from "../../useFetch"
import Cookies from 'js-cookie';
import axios from "axios";
import { useEffect, useState } from 'react';
import GitHubIcon from '@mui/icons-material/GitHub';
import { Avatar, Button, IconButton, RadioGroup } from "@mui/material";
import EditIcon from '@mui/icons-material/Edit';
import { Navigate, useNavigate } from "react-router-dom";
import useGetTokens from "../../useGetTokens";
import useGetAuthorData from "../../useGetAuthorData";


function getCsrfToken() {
  // const csrfToken = document.cookie.match(/csrftoken=([\w-]+)/);
  // return csrfToken ? csrfToken[1] : '';
  const csrftoken = Cookies.get('XSRF-TOKEN');
  return csrftoken;
}


export default function Profile() {

  const navigate = useNavigate();
  const {tokens, tokenError} = useGetTokens();
  const [authorData, setAuthorData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { authorID } = useGetAuthorData();
  const [connectionCount, setConnectionCount] = useState(0);

  // const { authorData, loading, error, authorID } = useGetAuthorData();
  useEffect(() => {
    const getAuthorData = async () => {
      try {
        const csrftoken = getCsrfToken();
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios.defaults.xsrfCookieName = 'csrftoken';        
        
        const response1 = await axios.get("/get_author_id/");
        const authorId = response1.data.author_id;
        const response2 = await axios.get("/authors/"+authorId+"/", {
          headers:{
              "Authorization": tokens[window.location.hostname]
          }
      });
        setAuthorData(response2.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    if (tokens) {
      getAuthorData();
    };
  }, [tokens]);

 
    const followerCount = async () => {
      try {
        const response = await axios.get("/authors/" + authorID + "/followers/", {
          headers: {
            "Authorization": tokens[window.location.hostname],
          },
        });
        console.log("FOLLOWERS",response.data);
        console.log("CONNN", response.data.items);
        setConnectionCount(response.data.items.length);
        console.log("CONNECTION COUNT", connectionCount);
        
      } catch (err) {
        // Handle the error here
      }
    };
    // Call the followerCount function
    followerCount();
  
    useEffect(() => {
      if (authorID) {
        followerCount();
      }
    }, [authorID]);
    

    
  // check if loading 
  if (loading) return; // placeholder for now 

  // check if any error generated shown in console
  if (error) console.log(error);

  return (
    <div>
        <div className="profileBox">
          <div className="editButtonContainer">
            <IconButton aria-label="edit" color="primary" onClick={()=> navigate('/profilepage')}>
              <EditIcon/>
            </IconButton>
          </div>
            <Avatar src={authorData?.profileImage} sx={{width:100, height:100}}/>
            <h1 className="nameTitle">
                {authorData?.displayName}
                {/* {data?.displayName} <-- what we actually need to display*/} 
            </h1>
            <div className="githubContainer">
              <IconButton 
              aria-label="github" 
              color="primary" 
              onClick={()=> window.open(authorData?.github, "_blank")}
              >
                <GitHubIcon/>
              </IconButton>
              <text className="githubText">@{authorData?.github.split("https://github.com/")}</text>
              </div>
              <div className="ConnectionCount">
                <h4 className="ConnectionCountText">{connectionCount}</h4>
                <text className="ConnectionCountTitle">Connections</text> 
              </div>
        </div>
    </div>
  )
}
