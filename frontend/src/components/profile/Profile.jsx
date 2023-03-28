import "./profile.css"
import useFetch from "../../useFetch"
import Cookies from 'js-cookie';
import axios from "axios";
import { useEffect, useState } from 'react';
import GitHubIcon from '@mui/icons-material/GitHub';
import { Avatar, Button, IconButton } from "@mui/material";
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

    
  // check if loading 
  if (loading) return; // placeholder for now 

  // check if any error generated shown in console
  if (error) console.log(error);

  // if (authorData) console.log(authorData);
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
        </div>
    </div>
  )
}
