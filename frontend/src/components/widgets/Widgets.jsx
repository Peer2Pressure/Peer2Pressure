import React, { useState, useEffect, useCallback } from 'react';
import SearchIcon from '@mui/icons-material/Search';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import './widgets.css';

function Widgets() {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [allUsers, setAllUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Fetch all users when the component mounts
    fetchAllUsers();
  }, []);

  const fetchAllUsers = async () => {
    try {
      const response = await fetch('http://localhost:8001/authors/');
      const data = await response.json();
      console.log('fetchAllUsers:', data);
      if (Array.isArray(data)) {
        setAllUsers(data);
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
    // Filter users based on the search term
    console.log('allUsers:', allUsers);
    if (allUsers) {
      const filteredUsers = allUsers.filter((user) => {      
        return user.username.toLowerCase().includes(query.toLowerCase());
      });
      console.log('Search term:', query);
      setSearchResults(filteredUsers);
    }
  }, [allUsers]);

  useEffect(() => {
    // Filter users whenever the search term changes
    filterUsers(searchTerm);
  }, [searchTerm, filterUsers]);

  const handleSubmit = (e) => {
    e.preventDefault();
    filterUsers(searchTerm);
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

      {isLoading ? (
        <div>Loading...</div>
      ) : (
        <div className="searchResults">
          {searchTerm === '' ? (
            <div>Enter a search term to find users.</div>
          ) : searchResults.length === 0 ? (
            <div>No results found.</div>
          ) : (
            searchResults.map((user) => (
              <div key={user.id} className="userResult">
                <span>{user.username}</span>
                <button className="followButton">
                  <PersonAddIcon />
                </button>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default Widgets;
