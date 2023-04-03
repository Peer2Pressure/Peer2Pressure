import "./github.css"

import React from 'react'
import { useEffect, useState} from "react";
import axios from "axios";

// const GitHub = ({username}) => {

//     // const [events, setEvents] = useState([]);

//     // useEffect(() => {
//     //     const fetchData = async () => {
//     //         try {
//     //             const response = await axios.get(`https://api.github.com/users/jteengfo/events`);
//     //             setEvents(response.data);
//     //         } catch(error) {
//     //             console.log('Error in retrieving github activity', error);
//     //         }
//     //     };
//     //     fetchData();
//     // }, [username]);

//     return(
//         <div id="feed">
//             GitHubActivity.feed({
                
//             })
//         </div>
//     );

// };

// export default GitHub

const GitHubActivityFeed = ({ username, limit }) => {
    useEffect(() => {
      // Ensure the GitHubActivity object is available before using it
      if (window.GitHubActivity && username !== '') {
        window.GitHubActivity.feed({
          username: username,
        //   repository: repository,
          selector: '#feed',
          limit: limit,
        });
      }
    }, [username, limit]);
  
    return (
      <div className="GitHubContainer">
        {/* <h2>GitHub Activity Feed for {username}</h2> */}
        { username !== '' ? (
            // Render the feed when the username is not null
            <>
                {/* <h2>GitHub Activity Feed for {username}</h2> */}
                <div id="feed"></div>
            </>
        ):(
             // Render the noUsernameContainer when the username is null
             <>
                <div className="noUsernameContainer">
                    <p id="text">User has no GitHub ID set. Nothing to display here. Here's some nuggets for you instead.</p>
                    <div className="puppyContainer">
                        <img src="https://i.chzbgr.com/full/8986835456/hAFC69A59/adorable-puppies-sleeping-in-a-mcdonalds-mcnuggets-box-and-looking-like-them-too" alt="pictures of puppies"></img>
                        {/* <img src="https://i.imgur.com/zY5fI6c.jpeg" alt="" /> */}
                    </div>
                </div>
             </>
        )}
      </div>
    );
  };
  
  export default GitHubActivityFeed;