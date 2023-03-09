import React,{useState, forwardRef } from "react";
import "./post.css";
import { Avatar } from "@mui/material";
import ChatBubbleOutlineIcon from "@mui/icons-material/ChatBubbleOutline";
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";


const Post = forwardRef(
  ({ id,displayName, username, text, image, avatar, likes, comments }, ref) => {
    const [like, setLike] = useState(false);
    const [likeCount, setLikeCount] = useState(likes);
    const handleLikeClick = () => {
      setLike(!like);
      if (like) {
        setLikeCount(likeCount + 1);
      } else {
        setLikeCount(likeCount - 1);
      }
    };
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
          <div className="post__likes" onClick={handleLikeClick}>
              {like ? (
                <>
                  <FavoriteIcon fontSize="small" />
                  <p>{likes + 1}</p>
                </>
              ) : (
                <>
                  <FavoriteBorderIcon fontSize="small" />
                  <p>{likes}</p>
                </>
              )}
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