import React, { useState, useEffect } from 'react';
import './notification.css';
import mockData from '../../mockData.json';
import Post from '../post/Post';
import Modal from '@mui/material/Modal';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import axios from 'axios';
import useGetAuthorData from '../../useGetAuthorData';
import useGetTokens from '../../useGetTokens';
function Notification(props) {
  const { authorData, authorID, tokens } = props;
  const [incomingNotifications, setIncomingNotifications] = useState([]);
  const [selectedPost, setSelectedPost] = useState(null);
  // const { authorData } = useGetAuthorData();
  // const { tokens } = useGetTokens();
  useEffect(() => {
    const interval = setInterval(async () => {
        try{
            const response = await axios.get(`${authorData.id}/inbox/?type=like_comment`, {
                headers: {
                    'Authorization': tokens[window.location.hostname],
                },
            });
            const notificationData =  response.data.items;
            setIncomingNotifications(notificationData);
        } catch (error) {
            console.error(error);
        }
    }, 1500);

    return () => clearInterval(interval);
}, []);


  const handleNotificationClick = async (postId) => {
    console.log('Notification clicked:', postId);
    try {
      const response = await axios.get(`${authorData.id}/posts/${postId}/`, {
        headers: {
            'Authorization': tokens[window.location.hostname],
            },});
      setSelectedPost(response.data);
        console.log("THIS IS THE RESPOBNE",response.data);
    } catch (error) {
      console.error(error);
    }
  };


  const handleModalClose = () => {
    setSelectedPost(null);
  };
  

  return (
    <div className="notification">
      <div className="notification__title">Notifications</div>
      <div className="notification__list">
      {incomingNotifications.map((notification) => {
        // Create a shallow copy of the notification object
        let updatedNotification = { ...notification };

        // If the notification type is 'comment', add a summary property
        if (notification.type === 'comment') {
          updatedNotification.summary = `${notification.author.displayName} commented on your post`;
        }
        return (
          updatedNotification.summary && (
            <div
              key={updatedNotification.id}
              className="notification__item"
              onClick={() => handleNotificationClick(updatedNotification.object.split('/').pop())}
            >
              <div className="notification__summary">{updatedNotification.summary}</div>
              <div className="notification__post">{updatedNotification.postTitle}</div>
            </div>
          )
        );
      })}
      </div>
      <Modal
        open={selectedPost !== null}
        onClose={handleModalClose}
        aria-labelledby="modal-title"
        aria-describedby="modal-description"
      >
        <Box sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 600,
          bgcolor: 'background.paper',
          border: '2px solid #000',
          boxShadow: 24,
          p: 4,
        }}>
          {selectedPost !== null && (
            <div>
                 <Button onClick={handleModalClose}>X</Button>
              <Typography variant="h6" id="modal-title" gutterBottom>
                {selectedPost.postTitle}
              </Typography>
              <Post 
              id={selectedPost.id}
                host={new URL(selectedPost.author.host).hostname}
                displayName={selectedPost.author.displayName}
                username={selectedPost.author.displayName}
                text={selectedPost.content}
                avatar={selectedPost.author.profileImage}
                comments={selectedPost.comments}
                contentType={selectedPost.contentType}
                title={selectedPost.title} 
                origin = {selectedPost.origin}
                visibility = {selectedPost.visibility}
                source = {selectedPost.source}
                postAuthorID2 = {selectedPost.author.id}
                authorData = {authorData}
                tokens = {tokens}
                />
            </div>
          )}
        </Box>
      </Modal>
    </div>
  );
}

export default Notification;
