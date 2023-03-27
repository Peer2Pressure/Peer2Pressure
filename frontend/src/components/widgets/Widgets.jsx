import React, { useState, useEffect, useCallback } from 'react';
import SearchIcon from '@mui/icons-material/Search';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import HowToRegIcon from '@mui/icons-material/HowToReg';
import './widgets.css';
import axios from 'axios';

function Widgets() {
  const [searchTerm, setSearchTerm] = useState('');
  const [isAuthorIdFetched, setIsAuthorIdFetched] = useState(false);
  const [allUsers, setAllUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [followedUsers, setFollowedUsers] = useState({});
  const [currentUserId, setCurrentUserId] = useState();
  const [singleAuthor, setsingleAuthor] = useState()
  const [displayedUsers, setDisplayedUsers] = useState([]);

  useEffect(() => {
    // Fetch all users when the component mounts
    fetchAllUsers();
  }, []);

  const getTokens = async () => {
    try {
      const response = await axios.get('/nodes/tokens/');
      console.log("TOKEN", response.data);
      const values = Object.values(response.data);
      return values.length > 0 ? values[0] : null;
    } catch (error) {
      console.error('Error fetching tokens:', error);
      return null;
    }
  };
  

  useEffect(() => {
    async function getauthorid() {
      try {
        const tokens = await getTokens();
        if (!tokens) {
          throw new Error('Failed to fetch tokens');
        }

        const response1 = await axios.get("/get_author_id/");
        setCurrentUserId(response1.data.author_id);

        const currentUserData = await fetchSingleAuthor(response1.data.author_id);
        setsingleAuthor(currentUserData);
        setIsAuthorIdFetched(true);
      } catch (error) {
        console.error("Error occurred: " + JSON.stringify(error));
      };
    };

    getauthorid();
  }, []);
  
  const fetchAllUsers = async (tokens) => {
    try {
      const response = await axios.get('/authors/'
      , {
        headers: {
          'Authorization': `Bearer ${tokens.access_token}`,
        },
      });
      const data = response.data;
      console.log('fetchAllUsers:', data);
      if (Array.isArray(data.items)) {
        setAllUsers(data.items);
        setIsLoading(false);
      } else {
        console.error('Error fetching users: response data is not an array');
        setIsLoading(false);
      }
    } catch (error) {
      console.error('Error fetching users:', error);
      setIsLoading(false);
    }
  };


  const filterUsers = useCallback((query) => {
    if (allUsers && singleAuthor) {
      const filteredUsers = allUsers.filter((user) => {
        return user.displayName !== singleAuthor.displayName && user.displayName.toLowerCase().includes(query.toLowerCase());
      });
      console.log('Search term:', query);
      setDisplayedUsers(filteredUsers);
    }
  }, [allUsers, singleAuthor]);

  useEffect(() => {
    filterUsers(searchTerm);
  }, [searchTerm, filterUsers, currentUserId]);

  const handleSubmit = (e) => {
    e.preventDefault();
    filterUsers(searchTerm);
  };

  const sendFollowRequest = async (user) => {
    console.log('sendFollowRequest called');

    if (followedUsers[user.id]) {
      console.log('User already followed');
      return;
    }

    const tokens = await getTokens();
    if (!tokens) {
      console.error('Error fetching tokens');
      return;
    }

    
    const singleAuthor = await fetchSingleAuthor(currentUserId);
      try {
        const data = {
          type: "Follow",
          summary: `${singleAuthor.displayName} wants to follow ${user.displayName}`,
          actor: singleAuthor,
          object: user,
        };
        console.log('Sending follow request:', data);
        console.log('User ID:', user.id);
        await axios.post(`${user.id}/inbox/`, data
        , {
          headers: {
            'Authorization': `Bearer ${tokens.access_token}`,
          },
        });
        console.log('Follow request sent successfully.');

        setFollowedUsers((prev) => ({ ...prev, [user.id]: true }));
      } catch (error) {
        console.error('Error sending follow request:', error);
      }
    };
  
    const fetchFollows = async (userId) => {
      try {
        const response = await axios.get(`/authors/${userId}/followers/`);
        const data = response.data;
        console.log('fetchFollows:', data);
        return data.following;
      } catch (error) {
        console.error('Error fetching follows:', error);
        return false;
      }
    };
  
    const fetchSingleAuthor = async (userId) => {
      try {
        const response = await axios.get(`/authors/${userId}/`);
        const data = response.data;
        setsingleAuthor(data);
        console.log('fetchSingleAuthor:', data);
        return data;
      } catch (error) {
        console.error('Error fetching singleAuthorId:', error);
        return false;
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
                  {user.id !== currentUserId && (
                    <button className="followButton" onClick={() => sendFollowRequest(user)}>
                      {followedUsers[user.id] ? (
                        <HowToRegIcon />
                      ) : (
                        <PersonAddIcon />
                      )}
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
  
  
