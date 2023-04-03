import React, { useState, useEffect, useCallback } from 'react';
import SearchIcon from '@mui/icons-material/Search';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import HowToRegIcon from '@mui/icons-material/HowToReg';
import './widgets.css';
import axios from 'axios';
import useGetTokens from '../../useGetTokens';
import useGetAuthorData from '../../useGetAuthorData';
import useGetNodeAPIEndpoints from '../../useGetNodeAPIEndpoints';

function Widgets() {
  const [searchTerm, setSearchTerm] = useState('');
  const [allUsers, setAllUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [followedUsers, setFollowedUsers] = useState(false);
  const [displayedUsers, setDisplayedUsers] = useState([]);

  const { tokens } = useGetTokens();
  const apiEndpoints  = useGetNodeAPIEndpoints();
  const { authorData, authorID } = useGetAuthorData();
  
  
  useEffect(() => {
    console.log('tokens:', tokens);
    console.log('authorData:', authorData);
    console.log('apiEndpoints:', apiEndpoints);
    
    if (tokens && authorData && apiEndpoints) {
      fetchAllUsers(tokens);
    }
  }, [tokens, authorData, apiEndpoints]);

  const fetchAllUsers = async () => {
    setIsLoading(true);
    let combinedUsers = [];
    apiEndpoints.forEach((endpoint) => {
      const hostname = new URL(endpoint).hostname;

      let url = `${endpoint}/authors/`;
      if (hostname === "www.distribution.social") {
        url = `${endpoint}/authors`;
      }

      try {
        // axios({
        //   method: "get",
        //   url: url, 
        //   maxRedirects: 3,
        //   headers: {
        //     'Authorization': tokens[hostname],
        //   },
        // })
        axios.get(url, {
          maxRedirects: 3,
          headers: {
            'Authorization': tokens[hostname],
          },
        })
        .then((response) => {
          if (response.status === 200) {
            combinedUsers.push(...response.data.items)
            setAllUsers(combinedUsers);
          } 
          else {
            console.error(`Error fetching users from ${url}: response status is not 200 or response data is not an array`);
          }
        }).catch((error) => {
          console.error(`Error fetching users from ${url}:`, error);
        });
      } 
      catch (error) {
        console.error(`Error fetching users from ${url}:`, error);
      }
    })
    
    setIsLoading(false);
    return combinedUsers;
  }
  

  const filterUsers = useCallback((query) => {
    if (allUsers && authorData) {
      const filteredUsers = allUsers.filter((user) => {
        return user.displayName !== authorData.displayName && user.displayName.toLowerCase().includes(query.toLowerCase());
      });
      setDisplayedUsers(filteredUsers);
    }
  }, [allUsers, authorData]);

  useEffect(() => {
    filterUsers(searchTerm);
  }, [searchTerm, filterUsers, authorID]);

  const handleSubmit = (e) => {
    e.preventDefault();
    filterUsers(searchTerm);
  };

  const sendFollowRequest = (user) => {
    // Check if already following
    const followURL = `/authors/${user.id.replace(/\/$/, "").split("/").pop()}/followers/${authorID}/`;
    axios.get(followURL, {
      headers: {
        'Authorization': tokens[window.location.hostname],
      },
    })
    .then((response) => {
      console.log('Already following user', response.data.items);
      if (response.status === 200) {
        setFollowedUsers(true);
        setFollowedUsers((prev) => ({ ...prev, [user.id]: true }));
        return;
      }
    })
    .catch((error) => {
      console.error('Author not following user', error);
    })
    .then(() => {
      // Send follow request
      const data = {
        type: "follow",
        summary: `${authorData.displayName} wants to follow ${user.displayName}`,
        actor: authorData,
        object: user,
      };
      console.log('Sending follow request:', data);
      console.log('User ID:', user.id);
      console.log('User host:', user.host);
      console.log('Author host:', authorData.host);
      console.log('Token:', tokens);
      console.log('Token TO SEND :', tokens[new URL(user.host).hostname]);
      
      let url = `${user.id.replace(/\/$/, "")}/inbox/`;
      if (new URL(user.id).hostname === "www.distribution.social") {
        url = `${user.id.replace(/\/$/, "")}/inbox`;
      }

      return axios.post(url, data, {
        maxRedirects: 3,
        headers: {
          'Authorization': tokens[new URL(user.host).hostname],
        },
      })
      .then((response) => {
        if (response.status === 200 || response.status === 201 ) {
          if (new URL(user.host).hostname !== window.location.hostname) {
            axios.put(followURL, data, {
              headers: {
                'Authorization': tokens[window.location.hostname],
                },
              }
            )
            .catch((error) => {
              console.error('Error updating follow request on local server:', error);
            });
          }
        }
      });
      ;
    })
    .then((response) => {
      console.log('Follow request sent successfully.', response.data);
      setFollowedUsers((prev) => ({ ...prev, [user.id]: true }));
    })
    .catch((error) => {
      console.error('Error sending follow request:', error);
    });
  };

  return (
    <div className="widgets">
      <form className="widgets__input" onSubmit={handleSubmit}>
        <SearchIcon className="widgets__searchIcon" />
        <input
          placeholder="Search for friends"
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </form>
  
      {!isLoading && (
        <div className="searchResults">
          {searchTerm === '' ? (
            <div></div>
          ) : displayedUsers.length === 0 ? (
            <div>No results found.</div>
          ) : (
            displayedUsers.map((user) => (
              <div key={user.id} className="userResult">
                <h3 className="hostnameText">
                  {user.displayName}{" "}
                  <span
                    className={
                      new URL(user.host).hostname !== window.location.hostname
                        ? "post__headerSpecial--different"
                        : "post__headerSpecial"
                    }
                  >
                    @{new URL(user.host).hostname}
                  </span>
                </h3>
                {user.id !== authorID && (
                  <button
                    className={`followButton ${followedUsers[user.id] ? "sent" : ""}`}
                    onClick={() => sendFollowRequest(user)}
                  >
                    <PersonAddIcon />
                  </button>
                )}
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
  
      }
      
export default Widgets;
              