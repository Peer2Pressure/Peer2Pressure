import React, { useState, useEffect } from 'react';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import HowToRegIcon from '@mui/icons-material/HowToReg';
import axios from 'axios';
import useGetTokens from '../../useGetTokens';
import useGetAuthorData from '../../useGetAuthorData';
import useGetNodeHosts from '../../useGetNodeHosts';
import './followRequest.css';

function FollowRequest() {
  const [incomingRequests, setIncomingRequests] = useState([]);
  const [followedUsers, setFollowedUsers] = useState({});
  const { tokens } = useGetTokens();
  const hostnames = useGetNodeHosts();
  const { authorData } = useGetAuthorData();

  useEffect(() => {
    if (tokens && authorData && hostnames) {
      fetchIncomingRequests(tokens);
    }
  }, [tokens, authorData, hostnames]);

  const fetchIncomingRequests = async () => {
    try {
      const requestPromises = hostnames.map(async (hostname) => {
        const response = await axios.get(`${authorData.id}/inbox/`, {
          headers: {
            'Authorization': tokens[hostname],
          },
        });
        console.log('response:', response.data);
        return response.data;
      });

      const results = await Promise.all(requestPromises);
      const combinedRequests = results.flatMap((data) => {
        if (Array.isArray(data.items)) {
          console.log('Fetched requests:', data.items);
          return data.items.filter(
            (item) =>
              item.type === 'Follow' &&
              item.object &&
              item.object.id === authorData.id
          );
        } else {
          console.error('Error fetching requests: response data is not an array');
          return [];
        }
      });
      console.log('Combined requests:', combinedRequests);
      setIncomingRequests(combinedRequests);
    } catch (error) {
      console.error('Error fetching requests:', error);
    }
  };

  const handleAccept = async (request) => {
    console.log('handleAccept called');
    try {
      const data = {
        type: 'Accept',
        summary: `${authorData.displayName} accepted ${request.actor.displayName}'s follow request`,
        actor: authorData,
        object: request,
      };
      console.log('Sending accept request:', data);
      await axios.post(`${request.actor.id}/inbox/`, data, {
        headers: {
          'Authorization': tokens[request.actor.host],
        },
      });
      console.log('Follow request accepted successfully.');
  
      // Make a PUT request to the followers API
      await axios.put(`${request.id}/inbox/followers/`,authorData.id.split('/').pop(), {
        headers: {
          'Authorization': tokens[authorData.host],
        },
      });
      console.log('Follower added to the local database.');
  
      setFollowedUsers((prev) => ({ ...prev, [request.object.id]: true }));
    } catch (error) {
      console.error('Error accepting follow request:', error);
    }
  };
  

  const handleDecline = async (request) => {
    console.log('handleDecline called');
    try {
      const data = {
        type: 'Decline',
        actor: authorData,
        object: request,
      };
      console.log('Sending decline request:', data);
      await axios.post(`${request.actor.id}/inbox/`, data, {
        headers: {
          'Authorization': tokens[request.actor.host],
        },
      });
      console.log('Follow request declined successfully.');
    } catch (error) {
      console.error('Error declining follow request:', error);
    }
  };

  return (
    <div className="followRequest">
      <div className="widgets__title">Follow Requests</div>
      {incomingRequests.length === 0 ? (
        <div>No incoming requests.</div>
      ) : (
        <div className="searchResults">
          {incomingRequests.map((request) => (
            <div key={request.id} className="request">
              <span>{request.actor.displayName}</span>
              <div>
                <button
                  className="acceptButton"
                  onClick={() => handleAccept(request)}
                >
                  <HowToRegIcon />
                </button>
                <button
                  className="declineButton"
                  onClick={() => handleDecline(request)}
                >
                  <PersonAddIcon />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
  
}
export default FollowRequest
