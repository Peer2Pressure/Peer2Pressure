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
    commentAuthorData, fullHost
}, ref) => {

    const[isLiked, setIsLiked] = useState(false);
    const[likeCounter, setLikeCounter] = useState(null);
    const[commentGetString, setCommentGetString] = useState(null);
    // const[commentAuthorData, setCommentAuthorData] = useState(null);  
    const {authorData, authorID} = useGetAuthorData();
    const {tokens, tokenError} = useGetTokens();
    

    const commentPostID = commentID.split("/")[8];
    console.log("commentID: ", `${commentID}/likes/`);
    console.log("commentAuthorHost: ", commentAuthorHost);
    useEffect(() => {
        const interval = setInterval(() => {
            async function getLikes() {
                try {
                    // const responseLikes = await axios.get(`/authors/${postAuthorID}/posts/${postID}/comments/${commentPostID}/likes/`);
                    if (commentAuthorHost === "https://distribution.social/api/") {
                        setCommentGetString(`${commentID}/likes`)
                    } else {
                        setCommentGetString(`${commentID}/likes/`)
                    }
                    const responseLikes = await axios.get(commentGetString);

                    // const responseLikes = await axios.get(`/authors/6a8f4948-0ac5-412f-9289-fb3c891c76de/posts/13369d36-86e8-4a8c-8abf-47d44d1822f6/
                    // comments/3eac07ec-035e-43a9-bc38-34b432e3cfd9/likes/`);
                    setLikeCounter(responseLikes.data.items.length);

                    // const responseCommentAuthorData = await axios.get(`authors/${commentAuthorID}/`);
                    // setCommentAuthorData(responseCommentAuthorData.data);

                } catch (error) {
                    console.log(error);
                }
            }
            getLikes();
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
                summary: `${commentDisplayName} liked your comment`,
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
    console.log("commentId: ", commentID);
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