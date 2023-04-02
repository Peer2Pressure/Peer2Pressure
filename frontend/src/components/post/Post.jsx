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
import ReactMarkdown from 'react-markdown'
import RepeatOutlinedIcon from '@mui/icons-material/RepeatOutlined';

import useGetAuthorData from "../../useGetAuthorData";
import useGetTokens from "../../useGetTokens";
import axios from "axios";
import { useEffect } from "react";
import Comment from "../comment/Comment";
import { v4 as uuidv4 } from 'uuid';

// menu source: https://mui.com/material-ui/react-menu/

// optios users can choose from upon clicking ellipsis
const options = [
  'Delete post',
];


// TODO: include logic clicking delete post



// TODO: include logic clicking delete post

const Post = forwardRef(
  ({ id, host, displayName, username, text, avatar, comments, contentType, title, origin, visibility }, ref) => {
    const [like, setLike] = useState(false);
    // const [likeCount, setLikeCount] = useState(likes);
    const [commentText, setCommentText] = useState("");
    const [showCommentArea, setShowCommentArea] = useState(false);
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [error, setError] = useState(null);
    const [inboxLikes, setInboxLikes] = useState([]);
    const [inboxComments, setInboxComments] = useState([]);
    const [likeCounter, setLikeCounter] = useState(0);
    const [authorLikedList, setAuthorLikedList] = useState([]);
    const [showShareOptions, setShowShareOptions] = useState(false);
    const [shareAnchorEl, setShareAnchorEl] = useState(null);
    const [shareVisibility, setShareVisibility] = useState(null);

    const {authorData, authorID} = useGetAuthorData();
    const {tokens} = useGetTokens();
    const postIdSplit = id.split("/")
    const postAuthorID = postIdSplit[4];
    const postID = postIdSplit[6];
    // console.log("postIDSplit: " + postIdSplit);
    // console.log("postAuthorID: " + postAuthorID);
    // console.log("postID: " + postID);

    const open = Boolean(anchorEl);
    const handleClick = (event) => {
      setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
      setAnchorEl(null);
    };

    // calls the inbox api to get all data in items
    useEffect(() => {
      const interval = setInterval(() => {
        async function getPosts() {
          try {
            // let's get the author ID 
            const response1 = await axios.get("/get_author_id/");
            const authorId = response1.data.author_id;
            
            // let's get all the posts under for current author ID
            const response2 = await axios.get("/authors/" + authorId + "/inbox/", {
              headers:{
                  "Authorization": tokens[window.location.hostname]
              }
            });
            // get all elements inside items of type "Like" and check if there exist a like in the specified object
            // const response3 = response2.data.items.filter((item) => item.type === "like" && item.id === object);
            // setInboxLikesID(response3);
            const response_likes = await axios.get(`/authors/${postAuthorID}/posts/${postID}/likes/`)
            setInboxLikes(response_likes.data.items); 
            setLikeCounter(response_likes.data.items.length);
            const responseLikesAuthors = response_likes.data.items.map((item) => item.author.id);
            const responseLikesAuthorsSplit = responseLikesAuthors.map((item) => item.split("/"));
            const responseLikesAuthorsSplit2 = responseLikesAuthorsSplit.map((item) => item[4]);
            setAuthorLikedList(responseLikesAuthorsSplit2);

            const response_comments = await axios.get(`/authors/${postAuthorID}/posts/${postID}/comments/`)
            setInboxComments(response_comments.data.comments);

            if (responseLikesAuthorsSplit2.includes(authorId)) {
              // console.log("author is here!")
              setLike(true);
            } else {
              setLike(false);
            };

          } catch(error) {
            setError(error);
          };
        };
    
        getPosts();
      }, 5000);
      return () => clearInterval(interval);
    }, [tokens, postAuthorID, postID]);

    // console.log("inboxLikes: ", inboxLikes);
    // console.log("inboxComments: ", inboxComments);
    // console.log(inboxLikes);
    // console.log("authorLikedList: ", authorLikedList);
    // upon like click execute this
    const handleLikeClick = async () => {

      if (like) {
        return;
      }
      // if (like) {
      //   // setLikeCount(likeCount + 1);
      //   console.log("triggered if");
      //   return;
      // } else {
      //   setLikeCount(likeCount - 1);
      //   console.log("triggered else")
      // }
      try {
        // encapsulated data to be sent
        const data = {
          type: "Like",
          summary: `${authorData.displayName} likes your post`,
          author: authorData,
          object: id
        };
        // send axios post 
        await axios.post(
          "/authors/" + postAuthorID + "/inbox/",
          data,
          {
            headers: {
              "Authorization": tokens[window.location.hostname]
            }
          });
          console.log("axios post worked. Like sent");
          setLike(true);
      } catch(error) {
        console.log(error);
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

    const handleShareClick = (event) => {
      setShowShareOptions(!showShareOptions);
      setShareAnchorEl(event.currentTarget);
    };

    useEffect(() => {
      if (shareVisibility !== null) {
        sendPost();
      }
    }, [shareVisibility]);
    

    // get followers to send a post
    async function getFollowers() {
      const response = await axios.get(`/authors/${authorID}/followers/`, {
          headers:{
              "Authorization": tokens[window.location.hostname]
          }
      });
      return response.data.items.map(obj => [obj.id.replace(/\/$/, "") +"/inbox/", new URL(obj.host).hostname]);
    }

    const sendPost = async () => {
      console.log("id", id);
      console.log("origin", origin);
      const postUUID = uuidv4();
      const data = {
          "type": "post",
          "id": `${authorData.id}/posts/${postUUID}`,
          "source": id,
          "origin": origin,
          "title": title,
          "contentType": contentType,
          "content": text,
          "author": authorData,
          "visibility": shareVisibility
      }

      console.log("DATA!", data);
      const p1 = axios
      .post(`/authors/${authorID}/inbox/`, data, {
          headers: {
              "Authorization": tokens[window.location.hostname]
          }
      })
      .catch((error) => {
          console.log(error)})
      
      const p2 = p1.then((response) => {
          setShareVisibility(null);
          const p3 = getFollowers();
          const p4 = p3.then((response2) => {
              
              //  Custom payload to post to Team 11 inbox
              const team11Data = {};
              team11Data["@context"] = "";
              team11Data["summary"] = "";
              team11Data["type"] = "post";
              team11Data["author"] = authorData;
              team11Data["object"] = response.data;
              
              console.log(team11Data);
              
              const localRequests = response2.map(obj => {
                  if (obj[1] === window.location.hostname) {
                      axios.post(obj[0], response.data, {
                          maxRedirects: 3,
                          headers: {
                              "Authorization": tokens[obj[1]]
                          }
                      })
                      .then((r) => {
                          console.log("Response", r)
                      });
                  }
              }) 
              
              const requestPromises = response2.map(obj => {
                  if (obj[1] !== window.location.hostname) {
                      axios.post(obj[0], obj[1] !== "quickcomm-dev1.herokuapp.com" ? response.data : team11Data, {
                          maxRedirects: 3,
                          headers: {
                              "Authorization": tokens[obj[1]]
                          }
                      });
                  }
              })
              Promise
              .all(requestPromises)
              .then((responses) => {
                  console.log('All requests sent successfully:', responses);
              })
              .catch((error) => {
                  console.error('Error sending requests:', error);
              })
          })
      })
    }

    return (
      <div className="post" ref={ref}>
        <div className="placeHolder">
          <div className="post__body">
            <div className="avatarAndNameContainer">
              <div className="post__avatar">
                <Avatar src={avatar} />
              </div>
              <div className="post__header">
                <div className="post_headerTop">
                  <div className="post__headerText">
                    <h3>
                      {displayName}{"  "}
                      <span className={host !== window.location.hostname ? "post__headerSpecial--different" : "post__headerSpecial"}>
                      @{host}
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
              </div>
            </div> 
            <div className="post__headerTitle">
              <b>{title}</b>
            </div>
            <div className="post__headerDescription">
              
              {contentType === "text/markdown" ?
                  <p><ReactMarkdown>{text}</ReactMarkdown></p>
                  :
                    <p>{text}</p>
              }
              
                {/* <img src={image} alt="" /> */}
            </div>
            <div className="commentsContainer">
              {/* were going go put comment component here */}
            </div>
          </div>
        </div>
        <div className="post__footer">
              <div className="iconArea">
                <div className="post__likes" onClick={handleLikeClick}>
                  {like ? (
                    <><FavoriteIcon fontSize="small"/>
                    {likeCounter}</>
                  ):(<><FavoriteBorderIcon fontSize="small" />
                      {likeCounter}</>
                  )}
                </div>
                <div className="post__comments" onClick={handleCommentClick}>
                <ChatBubbleOutlineIcon fontSize="small" />
                {/* <p>{comments}</p> */}
                </div>
                <div className="post__share" onClick={handleShareClick}>
                  <RepeatOutlinedIcon fontSize="small" />
                  <Menu
                    anchorEl={shareAnchorEl}
                    open={showShareOptions}
                  >
                    {visibility === "PUBLIC" && (
                      <MenuItem onClick={() => {
                        setShareVisibility("PUBLIC");
                      }}>
                        Share Publicly
                      </MenuItem>
                    )}
                    <MenuItem onClick={() => {
                        setShareVisibility("FRIENDS");
                      }}>
                        Share to Friends
                      </MenuItem>
                  </Menu>
                </div>
              </div>
              <div className="showCommentArea">
                  {showCommentArea && (
                  <form onSubmit={handleCommentSubmit}>
                    <div className="addCommentContainer">
                      {inboxComments.map((comment) => (
                        <div className="comment">
                          <Comment
                            commentAuthorID={comment.author.id}
                            commentID={comment.id}
                            commenntAvatar={comment.author.profileImage}
                            commentDisplayName={comment.author.displayName}
                            commentAuthorHost={new URL (comment.author.id).hostname}
                            comment={comment.comment}
                            commentPublished={comment.published}
                            postAuthorID={postAuthorID}
                            postID={postID}
                            commentAuthorData={comment.author}
                          />
                        </div>
                      ))}
                      <textarea className="post__commentInput"
                      placeholder="Add a comment..."
                      value={commentText}
                      onChange={(event) => setCommentText(event.target.value)}
                      />
                      <Button sx={{borderRadius: 20}} variant="contained" className="replybutton" type="submit">Reply</Button>
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
