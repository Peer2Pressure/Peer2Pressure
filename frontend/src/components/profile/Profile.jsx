import "./profile.css"
import useFetch from "../../useFetch"
import Cookies from 'js-cookie';
import axios from "axios";
import { useEffect, useState } from 'react';
import GitHubIcon from '@mui/icons-material/GitHub';
import { Avatar, Button } from "@mui/material";
import { Navigate, useNavigate } from "react-router-dom";

function getCsrfToken() {
  const csrftoken = Cookies.get('XSRF-TOKEN');
  return csrftoken;
}


export default function Profile() {

  const navigate = useNavigate();

  const [authorId, setAuthorId] = useState(null);
  const [authorData, setAuthorData] = useState(null);
  const [count, setCount] = useState(0);
  const [count1, setCount1] = useState(0);

  const {data: responseData1} = useFetch("/get_author_id/", {method: "get"});
  useEffect(() => {

    let self = this

    Promise.all(axios.get(), axios.get()).then(function (results){
      results[0]
    })

    axios.get("/get_author_id/", {method: "get"}).then(function(response){
      console.log(response)
      setAuthorData(reponse.data)
      self.setAuthorData(response.data)

      

    }).catch(function (err){
      //handle err
    })

    console.log("count: ", count);
    setCount(count+1);
    if (responseData1){
      console.log("get_author_id: ", count, ":",responseData1.author_id, ":")
      setAuthorId(responseData1.author_id);
      setAuthorData(responseData1.author_id);
      console.log("updated: ");
      // console.log(authorId, ":", authorData);
    }
  }, [responseData1]);


  const {data: responseData2, loading, error} = useFetch(authorId ? "/authors/"+authorId+"/" : null, {method: "get"});
  useEffect(() => {
    console.log("count 1: ", count1);
    console.log("Author data: ", authorData, authorId);
    if (responseData2){
      setCount1(count1+1);
      console.log("COUNT 1: ", count1, ":",responseData2, ":")
      setAuthorData(responseData2);
    };
  }, [authorData, responseData2]);

  // // check if loading 
  // if (loading) return <h1> Loading... </h1>; // placeholder for now 

  // // check if any error generated shown in console
  // if (error) console.log(error);

  if (authorData) {
    console.log(authorId, ":", authorData);
  }
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
