import "./followers.css";

import axios from "axios";

import { useState, useEffect, useCallback } from "react";

import SearchIcon from '@mui/icons-material/Search';

import useGetAuthorData from "../../useGetAuthorData";
import useGetTokens from "../../useGetTokens";
import useGetNodeAPIEndpoints from '../../useGetNodeAPIEndpoints';


function Followers({ onSelectUser, authorData, authorID, tokens }) {
    const [searchTerm, setSearchTerm] = useState('');
    const [allUsers, setAllUsers] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [followedUsers, setFollowedUsers] = useState(false);
    const [displayedUsers, setDisplayedUsers] = useState([]);

    // const {authorData, loading, authorError, authorID} = useGetAuthorData();
    // const {tokens, tokenError} = useGetTokens();
    const apiEndpoints  = useGetNodeAPIEndpoints();



    useEffect(() => {        
        if (tokens && authorData && apiEndpoints) {
          fetchAllUsers(tokens);
        }
    }, [tokens, authorData, apiEndpoints]);
    
    const fetchAllUsers = async () => {
        setIsLoading(true);
        let combinedUsers = [];
        apiEndpoints.forEach((endpoint) => {
            console.log("hsadasd: ", authorID)
            let url = `/authors/${authorID}/followers/`;
    
            try {
                axios.get(url, {
                    maxRedirects: 3,
                    headers: {
                        'Authorization': tokens[window.location.hostname]
                    },
                })
                .then((response) => {
                    if (response.status === 200) {
                        combinedUsers.push(...response.data.items)
                        setAllUsers(combinedUsers);
                    } else {
                        console.error(`Error fetching users from ${url}: response status is not 200 or response data is not an array`);
                    }
                }).catch((error) => {
                    console.error(`Error fetching users from ${url}:`, error);
                });
            } catch (error) {
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

    const selectUser = (user) => {
        onSelectUser(user);
    };

    return (
        <div className="followers">
            <form className="searchAuthor" onSubmit={handleSubmit}>
                <SearchIcon className="followerSearchIcon" />
                <input
                    placeholder="Search for User"
                    type="text"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </form>

            {!isLoading && (
                <div className="searchResults2">
                    {searchTerm === '' ? (
                        <div></div>
                        ) : displayedUsers.length === 0 ? (
                            <div>No results found.</div>
                        ) : (
                            displayedUsers.map((user) => (
                                <div key={user.id} className="userResult2" onClick={() => selectUser(user)}>
                                    <span>{user.displayName}</span>
                                </div>
                            ))
                        )
                    }
                </div>
            )}

        </div>
    )
}

export default Followers;