import React, { forwardRef } from "react";
import "./post.css";
import { Avatar } from "@mui/material";
import ChatBubbleOutlineIcon from "@mui/icons-material/ChatBubbleOutline";

import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";


const Post = forwardRef(
  ({ id,displayName, username, text, image, avatar, likes, comments }, ref) => {
    return (
      <div className="post" ref={ref}>
        <div className="post__avatar">
          <Avatar src={avatar} />
        </div>
        <div className="post__body">
          <div className="post__header">
            <div className="post__headerText">
              <h3>
                {displayName}{" "}
                <span className="post__headerSpecial">
                 @{username}
                </span>
              </h3>
            </div>
            <div className="post__headerDescription">
              <p>{text}</p>
            </div>
          </div>
          
          <img src={image} alt="" />
          <div className="post__footer">
            <div className="post__likes">
            <FavoriteBorderIcon fontSize="small" />
            <p>{likes}</p>
            </div>
            <div className="post__comments">
            <ChatBubbleOutlineIcon fontSize="small" />
            <p>{comments}</p>
            </div>  
          </div>
        </div>
      </div>
    );
  }
);

export default Post;
