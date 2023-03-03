import "./profile.css"
import useFetch from "../../useFetch"
import Cookies from 'js-cookie';
import axios from "axios";
import { useEffect, useState } from 'react';
import GitHubIcon from '@mui/icons-material/GitHub';
import { Avatar, Button } from "@mui/material";
import { Navigate, useNavigate } from "react-router-dom";

function getCsrfToken() {
  // const csrfToken = document.cookie.match(/csrftoken=([\w-]+)/);
  // return csrfToken ? csrfToken[1] : '';
  const csrftoken = Cookies.get('XSRF-TOKEN');
  return csrftoken;
}


export default function Profile() {

  // // calling the api to get data to be rendered in this component
  // const {response1, loading1, error1} = useFetch("http://localhost:8000/get_author_id/");
  // const authorId = response1.author_id;
  // const {response2, loading2, error2} = useFetch("http://localhost:8000/authors/"+ authorId + "/");
  // console.log(authorId, data, data1)

  const navigate = useNavigate();
  
  const [authorData, setAuthorData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getAuthorData = async () => {
      try {
        const csrftoken = getCsrfToken();
        axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        axios.defaults.xsrfCookieName = csrftoken;
        
        
        // const response1 = await axios.get("/get_author_id/");
        // const authorId = response1.data.author_id;
        const authorId = "7156bb35-4e95-4911-a6f6-ef9bdc77da75"
        const response2 = await axios.get("/authors/"+authorId+"/");
        setAuthorData(response2.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    getAuthorData();
  }, []);

    
  // check if loading 
  if (loading) return <h1> Loading... </h1>; // placeholder for now 

  // check if any error generated shown in console
  if (error) console.log(error);

  if (authorData) console.log(authorData);
  return (
    <div>
        <div className="profileBox">
            {/* <img class="profileImage" src={data?.profileImage} alt="profile of id.name"/> <-- what we actually need to display*/}
            {/* <img class="profileImage" src="/assets/johnDoe.jpg" alt="profile of id.name"/> */}
            <Avatar src={authorData?.profileImage} sx={{width:100, height:100}}/>
            <h1 className="nameTitle">
                {authorData?.displayName}
                {/* {data?.displayName} <-- what we actually need to display*/} 
            </h1>
              <Button className="manageProfileButton" onClick={()=> navigate('/profilepage')}>
                Manage profile
              </Button>
        </div>
    </div>
  )
}
