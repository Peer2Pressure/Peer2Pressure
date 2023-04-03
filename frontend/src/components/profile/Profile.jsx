import "./profile.css"
import useFetch from "../../useFetch"
import Cookies from 'js-cookie';
import axios from "axios";
import { useEffect, useState } from 'react';
import GitHubIcon from '@mui/icons-material/GitHub';
import { Avatar, Button, IconButton, RadioGroup, Modal, Box  } from "@mui/material";
import EditIcon from '@mui/icons-material/Edit';
import { Navigate, useNavigate } from "react-router-dom";
import useGetTokens from "../../useGetTokens";
import useGetAuthorData from "../../useGetAuthorData";


function getCsrfToken() {
  // const csrfToken = document.cookie.match(/csrftoken=([\w-]+)/);
  // return csrfToken ? csrfToken[1] : '';
  const csrftoken = Cookies.get('XSRF-TOKEN');
  return csrftoken;
}


export default function Profile(props) {
  const { authorData, authorID, tokens } = props;
  const navigate = useNavigate();
  console.log("profile etsing:, ", authorData)
  // const {tokens, tokenError} = useGetTokens();
  const [aData, setAuthorData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  // const { authorID } = useGetAuthorData();
  const [connectionCount, setConnectionCount] = useState(0);
  const [connectionsModalOpen, setConnectionsModalOpen] = useState(false);
  const [connections, setConnections] = useState([]);
  
    const handleLogoutClick = async () => {
    try {
      await axios.get("/accounts/logout/");
      navigate("/accounts/login/");
      // navigate(0);
      console.log("logged out");
    } catch (err) {
      console.log(err);
    } 
  };
  const handleConnectionsModalOpen = async () => {
    setConnectionsModalOpen(true);
    try {
      if (authorID) {
        const response = await axios.get("/authors/" + authorID + "/followers/", {
          headers: {
            "Authorization": tokens[window.location.hostname],
          },
        });
        setConnections(response.data.items)
        console.log("CONNECTIONS", response.data.items);
      }

    } catch (err) {
      // Handle the error here
    }
  };

  const handleConnectionsModalClose = () => {
    setConnectionsModalOpen(false);
  };
  // const { authorData, loading, error, authorID } = useGetAuthorData();
  useEffect(() => {
    const getAuthorData = async () => {
      try {
        // const csrftoken = getCsrfToken();
        // axios.defaults.xsrfHeaderName = 'X-CSRFToken';
        // axios.defaults.xsrfCookieName = 'csrftoken';        
        
        // const response1 = await axios.get("/get_author_id/");
        // const authorId = response1.data.author_id;
        const response2 = await axios.get("/authors/"+authorID+"/", {
          headers:{
              "Authorization": tokens[window.location.hostname]
          }
      });
        setAuthorData(response2.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    if (tokens) {
      getAuthorData();
    };
  }, [tokens]);

 
    const followerCount = async () => {
      try {
        if (authorID) {
          const response = await axios.get("/authors/" + authorID + "/followers/", {
            headers: {
              "Authorization": tokens[window.location.hostname],
            },
          });
          setConnectionCount(response.data.items.length);
        }
        
      } catch (err) {
        // Handle the error here
      }
    };
  
    useEffect(() => {
      if (authorID) {
        followerCount();
      }
    }, [authorID]);
    
    const handleDeleteConnection = (connection) => {
      // Implement the logic to delete the connection here.
      // For example, make an API call to delete the connection, and then update the state.
    };
    
  // check if loading 
  if (loading) return; // placeholder for now 

  // check if any error generated shown in console
  if (error) console.log(error);

  return (
    <div>
      <div className="profileBox">
        <div className="editButtonContainer">
          <IconButton aria-label="edit" color="primary" onClick={() => navigate('/profilepage')}>
            <EditIcon />
          </IconButton>
        </div>
        <Avatar src={aData?.profileImage} sx={{ width: 100, height: 100 }} />
        <h1 className="nameTitle">
          {aData?.displayName}
          {/* {data?.displayName} <-- what we actually need to display*/}
        </h1>
        <div className="githubContainer">
          <IconButton
            aria-label="github"
            color="primary"
            onClick={() => window.open(aData?.github, "_blank")}
          >
            <GitHubIcon />
          </IconButton>
          <div className="textContainer">
            <text className="githubText">
              {aData?.github && aData.github !== ""
                ? `@${aData.github.split("https://github.com/")[1]}`
                : ""}
            </text>
          </div>
          

        </div>
        <div className="ConnectionCount" onClick={handleConnectionsModalOpen}>
          <h4 className="ConnectionCountText">{connectionCount}</h4>
          <text className="ConnectionCountTitle">Connections</text>
        </div>
        <div className="logoutContainer">    
            <div className="logoutButton">
              <Button variant="text" onClick={handleLogoutClick}>Logout</Button>
            </div>
          </div>
      </div>
      <Modal
      open={connectionsModalOpen}
      onClose={handleConnectionsModalClose}
      aria-labelledby="connections-modal-title"
      aria-describedby="connections-modal-description"
    >
      <Box sx={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '50%',
        maxHeight: '80%',
        overflowY: 'auto',
        bgcolor: 'background.paper',
        border: '2px solid #000',
        boxShadow: 24,
        p: 4,
        borderRadius: '20px',
      }}>
        <h2 id="connections-modal-title" style={{ color: '#0058A2' }}>Connections</h2>
        <ul id="connections-modal-description" className="connectionsList">
          {connections.map((connection, index) => (
            <li key={index} className="connectionItem">
             <div className="avatarAndNameContainer">
        <div className="post__headerText">
          <h3>
            {connection.displayName}{" "}
            <span
              className={
                new URL(connection.host).hostname !== window.location.hostname
                  ? "post__headerSpecial--different"
                  : "post__headerSpecial"
              }
            >
              @{new URL(connection.host).hostname}
            </span>
          </h3>
        </div>
      </div>
              <button
                className="deleteConnectionButton"
                onClick={() => handleDeleteConnection(connection)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      </Box>
    </Modal>
          
  </div>
);
          }  
