import React, { forwardRef } from 'react'
import { Avatar } from '@mui/material'
import './comment.css'

import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import { useEffect, useState } from 'react';
import axios from 'axios';
import useGetTokens from '../../useGetTokens';
import useGetAuthorData from '../../useGetAuthorData';

// const Comment = forwardRef(({profileImage, displayName, comment }, ref) => {

const Comment = forwardRef(({
    commentAuthorID, commentID, commentAvatar, commentDisplayName, 
    commentAuthorHost, comment, commentPublished, postAuthorID, postID,
    commentAuthorData,
}, ref) => {

    const[isLiked, setIsLiked] = useState(false);
    const[likeCounter, setLikeCounter] = useState(null);
    // const[commentAuthorData, setCommentAuthorData] = useState(null);  
    const {authorData, authorID} = useGetAuthorData();
    const {tokens, tokenError} = useGetTokens();

    useEffect(() => {
        const interval = setInterval(() => {
            async function getLikes() {
                try {
                    const responseLikes = await axios.get(`authors/${postAuthorID}/posts/${postID}/
                    comments/${commentID}/likes/`);
                    setLikeCounter(responseLikes);

                    // const responseCommentAuthorData = await axios.get(`authors/${commentAuthorID}/`);
                    // setCommentAuthorData(responseCommentAuthorData.data);

                } catch (error) {
                    console.log(error);
                }
            }
        }, 5000);
        return () => clearInterval(interval);
    }, [tokens]);

    const handleCommentLikeClick = async () => {

        // skip if already liked
        if (isLiked) {
            return;
        }
        // set like to true
        try {
            const data = {
                type: "Like",
                summary: `{commentDisplayName} liked your comment`,
                author: authorData,
                object: commentID,
            };

            await axios.post(
                `authors/${postAuthorID}/inbox/`, data,
                {
                    headers: {
                        "Authorization": tokens[window.location.hostname]
                    }
                }
            );
            console.log("Comment like sent successfully")
            // set like to true
            setIsLiked(true);
        } catch(error) {
            console.log(error);
        }
    };
    console.log("likeCounter: ", likeCounter)
    return (
        <div className="commentContainer">
            <div className="commentHeader">
                <div className="avatarContainer">
                    <Avatar sx={{width: 32, height: 32}} src={commentAvatar}/>
                    {/* <Avatar sx={{width: 24, height: 24}}/> */}
                </div>
                <div className="authorAndCommentContainer">
                    <div className="authorContainer">
                        {/* <h5>John Doe</h5> */}
                        <h4 id='authorNAme'>{commentDisplayName}{" "}
                        <span className={commentAuthorHost !== window.location.hostname ? "post__headerSpecial--different" : "post__headerSpecial"}>
                        @{commentAuthorHost}
                        </span>
                        </h4>
                    </div>
                    <div className="commentBody">
                        {/* <p>To be or not to be, that is the question.</p> */}
                        <p>{comment}</p>
                    </div>
                </div>
            </div>
            <div className="iconContainer" onClick={handleCommentLikeClick}>
                {isLiked? (<><FavoriteIcon fontSize="small" /></>)
                :(<><FavoriteBorderIcon fontSize="small" /></>)}
                <p>{likeCounter}</p>
                {/* <FavoriteIcon fontSize='small'/> */}
            </div>
        </div>
    )
});

export default Comment;