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
    try {
      setIsLoading(true);
      const requestPromises = apiEndpoints.map(async (endpoint) => {
        const hostname = new URL(endpoint).hostname
        let url = `${endpoint}/authors`;
        
        // // Update host if host is localhost
        // if (hostname === "localhost") {
        //   url = `http://${window.location.host}/authors`;
        //   console.log("this is a localhost", url)
        // };

        const response = await axios.get(url, {
          headers: {
            'Authorization': tokens[hostname],
          },
        });
        return response.data;
      });
  
      const results = await Promise.all(requestPromises);
      const combinedUsers = results.flatMap((data) => {
        if (Array.isArray(data.items)) {
          console.log('Fetched users:', data.items);
          return data.items;
        } else {
          console.error('Error fetching users: response data is not an array');
          return [];
        }
      });
      console.log('Combined users:', combinedUsers);
      setAllUsers(combinedUsers);
    } catch (error) {
      console.error('Error fetching users:', error);
    } finally {
      setIsLoading(false);
    }
  };
  

  const filterUsers = useCallback((query) => {
    if (allUsers && authorData) {
      const filteredUsers = allUsers.filter((user) => {
        return user.displayName !== authorData.displayName && user.displayName.toLowerCase().includes(query.toLowerCase());
      });
      console.log('Filtered users:', filteredUsers);
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

  const sendFollowRequest = async (user) => {
    console.log('sendFollowRequest called');
      
    try {
      // Check if already following
      const response = await axios.get(`/authors/${user.id.replace(/\/$/, "").split("/").pop()}/followers/`, {
        headers: {
          'Authorization': tokens[window.location.hostname],
        },
      });
      console.log('Already following user', response.data.items);
      const following = response.data.items.some((item) => item.id === authorData.id);
      if (following) {
        setFollowedUsers(true);
        setFollowedUsers((prev) => ({ ...prev, [user.id]: true }));
        return;
      }
      const data = {
        type: "Follow",
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
      await axios.post(`${user.id}/inbox`, data, {
        headers: {
          'Authorization': tokens[new URL(user.host).hostname],
        },
      });
      console.log('Follow request sent successfully.');
      setFollowedUsers((prev) => ({ ...prev, [user.id]: true }));
    } catch (error) {
      console.error('Error sending follow request:', error);
    }
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
                      <span>{user.displayName}</span>
                      {user.id !== authorID && (
                        <button className={`followButton ${followedUsers[user.id] ? 'sent' : ''}`} onClick={() => sendFollowRequest(user)}>
                        <PersonAddIcon/>
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
              
