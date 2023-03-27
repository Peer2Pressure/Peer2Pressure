import React, { useState, forwardRef } from "react";
import "./post.css";
import { Avatar, Menu } from "@mui/material";
import ChatBubbleOutlineIcon from "@mui/icons-material/ChatBubbleOutline";
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import MoreVertIcon from '@mui/icons-material/MoreVert';
import IconButton from '@mui/material/IconButton';
import MenuItem from '@mui/material/MenuItem';
import Button from "@mui/material/Button";

// menu source: https://mui.com/material-ui/react-menu/

// optios users can choose from upon clicking ellipsis
const options = [
  'Delete post',
];


// TODO: include logic clicking delete post



// TODO: include logic clicking delete post

const Post = forwardRef(
  ({ id, displayName, username, text, image, avatar, likes, comments }, ref) => {
    const [like, setLike] = useState(false);
    const [likeCount, setLikeCount] = useState(likes);
    const [commentText, setCommentText] = useState("");
    const [showCommentArea, setShowCommentArea] = useState(false);

    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
      setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
      setAnchorEl(null);
    };

    const handleLikeClick = () => {
      setLike(!like);
      if (like) {
        setLikeCount(likeCount + 1);
      } else {
        setLikeCount(likeCount - 1);
      }
    };

    const handleCommentClick = () => {
      setShowCommentArea(!showCommentArea);
    };

    const handleCommentSubmit = (event) => {
      event.preventDefault();
      console.log(commentText); // Need to replace this with a post request to the API
      setCommentText("");
    };


    return (
      <div className="post" ref={ref}>
        <div className="placeHolder">
          <div className="post__avatar">
            <Avatar src={avatar} />
          </div>
          <div className="post__body">
          <div className="post__header">
            <div className="post_headerTop">
              <div className="post__headerText">
                <h3>
                  {displayName}{" "}
                  <span className="post__headerSpecial">
                  @{username}
                  </span>
                </h3>
              </div>
              <span className="post_headerMenu">
                    <IconButton
                      aria-label="more"               // acccessibility: https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-label
                      id="long-button"
                      aria-controls={open ? 'long-menu' : undefined}
                      aria-expanded={open ? 'true' : undefined}
                      aria-haspopup="true"
                      onClick={handleClick}
                      >
                      <MoreVertIcon />
                    </IconButton>
                    <Menu
                      id="long-menu"
                      MenuListProps={{
                        'aria-labelledby': 'long-button',
                      }}
                      anchorEl={anchorEl}
                      open={open}
                      onClose={handleClose}
                      PaperProps={{
                        style: {
                          // maxHeight: ITEM_HEIGHT * 4.5,
                          width: '20ch',
                        },
                      }}
                    >
                      {options.map((option) => (
                        <MenuItem key={option}>
                          {option}
                        </MenuItem>
                      ))}
                    </Menu>
              </span>
            </div>
            <div className="post__headerDescription">
              <p>{text}</p>
            </div>
          </div>
          <img src={image} alt="" />
          </div>
        </div>
        <div className="post__footer">
              <div className="iconArea">
                <div className="post__likes" onClick={handleLikeClick}>
                  {like ? (
                    <>
                      <FavoriteIcon fontSize="small" />
                      {/* <p>{likes + 1}</p> */}
                    </>
                  ) : (
                    <>
                      <FavoriteBorderIcon fontSize="small" />
                      <p>{likes}</p>
                    </>
                  )}
                </div>
                <div className="post__comments" onClick={handleCommentClick}>
                <ChatBubbleOutlineIcon fontSize="small" />
                {/* <p>{comments}</p> */}
                </div>
              </div>
              <div className="showCommentArea">
                  {showCommentArea && (
                  <form onSubmit={handleCommentSubmit}>
                    <div className="addCommentContainer">
                      <textarea className="post__commentInput"
                      placeholder="Add a comment..."
                      value={commentText}
                      onChange={(event) => setCommentText(event.target.value)}
                      />
                      <Button className="replybutton" type="submit">Reply</Button>
                    </div>
                  </form>
                )}
              </div>
        </div>
      </div>
    );
  }
);

export default Post;
