import "./profile.css"
import useFetch from "../../useFetch"
import GitHubIcon from '@mui/icons-material/GitHub';
import { Avatar, Button } from "@mui/material";

export default function Profile() {

  // calling the api to get data to be rendered in this component
  const {data, loading, error} = useFetch("http://localhost:8000/authors/ea89c93d-4879-450d-9d12-58bb06d484c1");
  
  // check if loading 
  if (loading) return <h1> Loading... </h1>; // placeholder for now 

  // check if any error generated shown in console
  if (error) console.log(error);

  return (
    <div>
        <div className="profileBox">
            {/* <img class="profileImage" src={data?.profileImage} alt="profile of id.name"/> <-- what we actually need to display*/}
            {/* <img class="profileImage" src="/assets/johnDoe.jpg" alt="profile of id.name"/> */}
            <Avatar alt={data?.displayName} src="/assets/johnDoe.jpg" sx={{width:100, height:100}}/>
            <h1 className="nameTitle">
                {data?.first_name} {data?.last_name}
                {/* {data?.displayName} <-- what we actually need to display*/} 
            </h1>
            <h2 className="gitHubProfile">
              <span className="gitHubBox">
                <Button variant="text">
                  <GitHubIcon/> {data?.email}
                </Button>
              </span>
            </h2>
            <Button className="manageProfileButton">Manage profile</Button>
        </div>
    </div>
  )
}
