import "./profile.css"
import useFetch from "../../useFetch"

import axios from "axios";
import Cookies from 'js-cookie';
import { useEffect, useState } from 'react';
import GitHubIcon from '@mui/icons-material/GitHub';
import { Avatar, Button } from "@mui/material";

function getCsrfToken() {
  // const csrfToken = document.cookie.match(/csrftoken=([\w-]+)/);
  // return csrfToken ? csrfToken[1] : '';
  const csrftoken = Cookies.get('csrftoken');
  return csrftoken;
}


export default function Profile() {

  // // calling the api to get data to be rendered in this component
  // const {response1, loading1, error1} = useFetch("http://localhost:8000/get_author_id/");
  // const authorId = response1.author_id;
  // const {response2, loading2, error2} = useFetch("http://localhost:8000/authors/"+ authorId + "/");
  // console.log(authorId, data, data1)
  
  const [authorData, setAuthorData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const getAuthorData = async () => {
      try {
        
        const csrftoken = getCsrfToken();
        
        const response1 = await axios.get("/get_author_id/", {
          'X-CSRFToken': csrftoken,
        });
        const authorId = response1.data.author_id;
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

  return (
    <div>
        <div className="profileBox">
            {/* <img class="profileImage" src={data?.profileImage} alt="profile of id.name"/> <-- what we actually need to display*/}
            {/* <img class="profileImage" src="/assets/johnDoe.jpg" alt="profile of id.name"/> */}
            <Avatar src={authorData?.avatar} sx={{width:100, height:100}}/>
            <h1 className="nameTitle">
                {authorData?.first_name} {authorData?.last_name}
                {/* {data?.displayName} <-- what we actually need to display*/} 
            </h1>
            <Button className="manageProfileButton">Manage profile</Button>
        </div>
    </div>
  )
}
