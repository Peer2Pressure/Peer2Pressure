import "./profile.css"
import useFetch from "../../useFetch"

export default function Profile() {

  // calling the api to get data to be rendered in this component
  const {data, loading, error} = useFetch("https://random-data-api.com/api/v2/users?size=1&is_xml=true");
  
  // check if loading 
  if (loading) return <h1> Loading... </h1>; // placeholder for now 

  // check if any error generated shown in console
  if (error) console.log(error);

  return (
    <div>
        <div className="profileBox">
            <img class="profileImage" src="/assets/johnDoe.jpg" alt="profile of id.name"/>
            <h1 className="nameTitle">
                {data?.first_name} {data?.last_name}
            </h1>
            <button className="manageProfileButton">Manage profile</button>
        </div>
    </div>
  )
}
