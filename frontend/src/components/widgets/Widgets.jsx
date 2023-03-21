import React, { useState, useEffect, useCallback } from 'react';
import SearchIcon from '@mui/icons-material/Search';
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
      // Replace this with the actual API endpoint that returns all users.
      const response = await fetch('http://localhost:8000/authors/');
      const data = await response.json();

      // Assumes the API returns an array of users. Adjust as needed
      setAllUsers(data);
      setIsLoading(false);
    } catch (error) {    
      console.error('Error fetching users:', error);
      setIsLoading(false);
    }
  };

  const filterUsers = useCallback((query) => {
    // Filter users based on the search term
    if (allUsers) {
      if (query) {
        const filteredUsers = allUsers.filter((user) => {
          return user.username.toLowerCase().includes(query.toLowerCase());
        });
        console.log('Search term:', query);
        setSearchResults(filteredUsers);
      } else {
        setSearchResults([]);
      }
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
          {searchResults.map((user) => (
            <div key={user.id}>
              {/* Render user details here */}
              {user.username}
            </div>
          ))}
          {searchResults.length === 0 && <div></div>}
        </div>
      )}
    </div>
  );
}

export default Widgets;
