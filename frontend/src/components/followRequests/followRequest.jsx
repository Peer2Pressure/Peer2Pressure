import React, { useState, useEffect } from 'react';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import HowToRegIcon from '@mui/icons-material/HowToReg';
import axios from 'axios';
import useGetTokens from '../../useGetTokens';
import useGetAuthorData from '../../useGetAuthorData';
import useGetNodeAPIEndpoints from '../../useGetNodeAPIEndpoints';
import './followRequest.css';

function FollowRequest() {
  const [incomingRequests, setIncomingRequests] = useState([]);
  const [followedUsers, setFollowedUsers] = useState({});
  const { tokens } = useGetTokens();
  const apiEndpoints = useGetNodeAPIEndpoints();
  const { authorData } = useGetAuthorData();
  const [acceptedRequests, setAcceptedRequests] = useState({});
  const [removedRequests, setRemovedRequests] = useState({});

  useEffect(() => {
    if (tokens && authorData && apiEndpoints) {
      const interval = setInterval(() => {
        fetchIncomingRequests(tokens);
      }, 1500);
      return () => clearInterval(interval);
    }
  }, [tokens, authorData, apiEndpoints]);

  const fetchIncomingRequests = async () => {
    // console.log('author Data:', authorData);
    try {
      const response = await axios.get(`${authorData.id}/inbox/?type=request`, {
        headers: {
          'Authorization': tokens[window.location.hostname],
        },
      });
      // console.log('response:', response.d);
      const data = response.data;
      if (Array.isArray(data.items)) {
        // console.log('Fetched requests:', data.items);
        setIncomingRequests(response.data.items);
      } else {
        console.error('Error fetching requests: response data is not an array');
      }
    } catch (error) {
      console.error('Error fetching requests:', error);
    }
  };
  
  

  const handleAccept = async (request) => {
    console.log('handleAccept called');
    if (authorData) {
      try {
        const data = {
          type: 'follow',
          summary: `${authorData.displayName} accepted ${request.displayName}'s follow request`,
          actor: request,
          object: authorData,
          approved: true,
        };
        let url = `${request.id.replace(/\/$/, "")}/inbox/`;
      
        if (new URL(request.id).hostname === "www.distribution.social") {
          url = `${request.id.replace(/\/$/, "")}/inbox`;
        }
        // console.log('author Data:', authorData);

        console.log('Sending accept request:', data);
        await axios.post(url, data, {
          maxRedirects: 3,
          headers: {
            'Authorization': tokens[new URL(request.host).hostname],
          },
        });
        console.log('Follow request accepted successfully.');
        if (new URL(request.host).hostname !== window.location.hostname) {
          // Make a PUT request to the followers API
          await axios.put(`${authorData.id}/followers/${request.id.replace(/\/$/, "").split("/").pop()}/`, data,  {
            headers: {
              'Authorization': tokens[window.location.hostname],
            },
          });
       }
        console.log('Follower added to the local database.');
        setAcceptedRequests((prev) => ({ ...prev, [request.id]: true }));
        setFollowedUsers((prev) => ({ ...prev, [request.id]: true }));
        setTimeout(() => {
          setRemovedRequests((prev) => ({ ...prev, [request.id]: true }));
          setIncomingRequests((prev) => prev.filter((r) => r.id !== request.id));
        }, 2000);
      } catch (error) {
        console.error('Error accepting follow request:', error);
      }
  }};
  

  // const handleDecline = async (request) => {
  //   console.log('handleDecline called');
  //   try {
  //     const data = {
  //       type: 'Decline',
  //       actor: authorData,
  //       object: request,
  //     };
  //     console.log('Sending decline request:', data);
  //     await axios.post(`${request.actor.id}/inbox/`, data, {
  //       headers: {
  //         'Authorization': tokens[request.actor.host],
  //       },
  //     });
  //     console.log('Follow request declined successfully.');
  //   } catch (error) {
  //     console.error('Error declining follow request:', error);
  //   }
  // };

  return (
    <div className="followRequest">
      <div className="widgets__title">Follow Requests</div>
      {incomingRequests.length === 0 ? (
        <div>No pending requests.</div>
      ) : (
        <div className="searchResults">
          {incomingRequests
            .filter((request) => !removedRequests[request.id])
            .map((request) => (
              <div key={request.id} className="request">
                <span>{request.displayName}</span>
                <div>
                  <button
                    className={`acceptButton ${acceptedRequests[request.id] ? "accepted" : ""}`}
                    onClick={() => handleAccept(request)}
                  >
                    <HowToRegIcon />
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
