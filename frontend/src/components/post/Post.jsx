import React, { useState, forwardRef } from "react";
import "./post.css";
import { Avatar, Menu } from "@mui/material";
import ChatBubbleOutlineIcon from "@mui/icons-material/ChatBubbleOutline";
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import MenuItem from '@mui/material/MenuItem';
import Button from "@mui/material/Button";
import ReactMarkdown from 'react-markdown'
import RepeatOutlinedIcon from '@mui/icons-material/RepeatOutlined';

import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';

import EditPost from "../editPost/EditPost";
import ModeEditIcon from '@mui/icons-material/ModeEdit';
import DeleteIcon from '@mui/icons-material/Delete';
import axios from "axios";
import { useEffect } from "react";
import Comment from "../comment/Comment";
import { v4 as uuidv4 } from 'uuid';

// menu source: https://mui.com/material-ui/react-menu/

const Post = forwardRef(
  ({ id, host, displayName, username, text, avatar, comments, contentType, title, origin, visibility, source, postAuthorID2, authorData, authorID, tokens }, ref) => {
    const [like, setLike] = useState(false);
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
    const [originAuthorDisplayName, setOriginAuthorDisplayName] = useState(null);
    const [originAuthorHost, setOriginAuthorHost] = useState(null);

    const originAuthor = origin.replace(/\/posts\/.*$/, "/");
    const [postLikeString, setPostLikeString] = useState("");
    const [postCommentString, setPostCommentString] = useState("");


    const postIdSplit = id.replace(/\/$/, "").split("/");
    const postID = id.replace(/\/$/, "").split("/").pop();
    const postAuthorID = postIdSplit[postIdSplit.length - 3];

    const deletePost = () => {
      confirmAlert({
        title: 'Delete Post?',
        // message: 'Delete Post?',
        buttons: [
          {
            label: 'Yes',
            onClick: () => {
              axios.delete(id+"/", {
                headers: {
                  "Authorization": tokens[window.location.hostname]
                }
              })
                .then((response) => {
                  console.log(response);
                })
                .catch((error) => {
                  console.log(error);
                })
            }
          },
          {
            label: 'No',
          }
        ]
      });
    }

    // calls the inbox api to get all data in items
    useEffect(() => {
      const interval = setInterval(() => {
        async function getPostComments() {
          try {
            // // let's get the author ID 
            // const response1 = await axios.get("/get_author_id/");
            // const authorId = response1.data.author_id;
            
            // // let's get all the posts under for current author ID
            // const response2 = await axios.get("/authors/" + authorId + "/inbox/", {
            //   headers:{
            //       "Authorization": tokens[window.location.hostname]
            //   }
            // });
            // get all elements inside items of type "Like" and check if there exist a like in the specified object
            // const response3 = response2.data.items.filter((item) => item.type === "like" && item.id === object);
            // setInboxLikesID(response3);

            // getting likes 
            const response_likes = await axios.get(`${id}/likes/`);
            setInboxLikes(response_likes.data.items); 
            setLikeCounter(response_likes.data.items.length);
            const responseLikesAuthors = response_likes.data.items.map((item) => item.author.id);
            const responseLikesAuthorsSplit = responseLikesAuthors.map((item) => item.split("/"));
            const responseLikesAuthorsSplit2 = responseLikesAuthorsSplit.map((item) => item[4]);
            setAuthorLikedList(responseLikesAuthorsSplit2);

            // getting comments
            const response_comments = await axios.get(`${id}/comments/`)
            // const response_comments = await axios.get(`/authors/${postAuthorID}/posts/${postID}/comments/`)
            setInboxComments(response_comments.data.comments);

            setPostCommentString(`/authors/${postAuthorID}/inbox/`);
            console.log("This is the postCommentString\n\n\n", postCommentString);
            if (host === "https://distribution.social/api/") {
            setPostCommentString(`/authors/${postAuthorID}/inbox`);
            } 

            setPostLikeString(`/authors/${postAuthorID}/inbox/`);
            // send axios post 
            if (host === "https://distribution.social/api/") {
              setPostLikeString(`/authors/${postAuthorID}/inbox`);
            }

            if (responseLikesAuthorsSplit2.includes(authorID)) {
              // console.log("author is here!")
              setLike(true);
            } else {
              setLike(false);
            };

          } catch(error) {
            setError(error);
          };
        };
    
        getPostComments();
      }, 3000);
      return () => clearInterval(interval);
    }, [tokens, postAuthorID, postID]);


    // upon like click execute this
    const handleLikeClick = async () => {
      if (like) {
        return;
      }

      try {
        // encapsulated data to be sent
        const data = {
          type: "Like",
          summary: `${authorData.displayName} likes your post`,
          author: authorData,
          object: id
        };

        await axios.post(
          postLikeString,
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

    const handleCommentSubmit = async (event) => {
      event.preventDefault();
      console.log("comment submitted;", id);
      console.log("Hostname;",comments);
      console.log("This is the m_id;", authorID);
      console.log("This is the m_data;", authorData);
      console.log("This is the KEY;", id);
      // setPostCommentString(`/authors/${postAuthorID}/inbox/`);
        try {
          const data = {
            type: 'comment',
               author: {
                    type: 'author',
                    id: authorData.id,
                    url: authorData.id,
                    host: authorData.host,
                    displayName: authorData.displayName,
                    github: null,
                    profileImage: null    
            },
            comment: commentText,
            contentType: 'text/markdown',
            object: id
          };

          const response = await axios.post(postCommentString, data, {
            headers: {
              'Authorization': tokens[new URL (comments).hostname],
            }
          });
    
        // Do something with the response, such as displaying the new comment
        console.log("This is post",response.data);
    
        // Clear the comment text area
        setCommentText('');
      } catch (error) {
        console.error(error);
      }
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

    const getOriginAuthor = async () => {
      axios.get(`${originAuthor}`, {
        headers: {
          "Authorization": tokens[window.location.hostname]
        }
      })
      .then((response) => {
        setOriginAuthorDisplayName(response.data.displayName);
        setOriginAuthorHost(new URL(response.data.host).hostname);
      })
      .catch((error) => {
      console.log("probably a nothing error when getting source author bc ur not authorized even tho i send in authorization?");
      });
    }
    
    useEffect(() => {
      getOriginAuthor();
    }, [originAuthor, tokens]);

    const sendPost = async () => {
      const postUUID = uuidv4();
      const data = {
          "type": "post",
          "id": `${authorData.id}/posts/${postUUID}`,
          // "source": id,
          "source": `${authorData.id}/posts/${postUUID}`,
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
                </div>
              </div>
              <span className="post_headerMenu">
                <div className="post__edit">
                  {authorData?.id === postAuthorID2 && (
                    <Popup 
                    trigger={<ModeEditIcon fontSize="small"/>}
                    modal={true}
                    closeOnDocumentClick={false}
                    >
                      {close => (
                        <>
                          <EditPost 
                            postID={id} 
                            postTitle={title} 
                            postText={text} 
                            postContentType={contentType} 
                            postAuthorID={postAuthorID2}
                            onClose={close}/>
                          <button className="closeButton" onClick={close}>x</button>
                        </>
                      )}
                  </Popup>
                  )}
                </div>
                {/* <div className="post__delete">
                {authorData?.id === postAuthorID2 && (
                    
                    <DeleteIcon fontSize="small" onClick={deletePost}/>
                  )}
                </div> */}
              </span>
            </div>
            <div className="post__headerTitle">
              <b>{title}</b>
            </div>
            <div className="post__headerDescription">
              
            {contentType === "text/markdown" ?
              <p><ReactMarkdown>{text}</ReactMarkdown></p>
              :
              contentType === "image/png;base64" || contentType === "image/jpeg;base64" ?
              <img src={text} alt="" />
              :
              <p>{text}</p>
            }              
                
            </div>
            <div className="commentsContainer">
              {/* were going go put comment component here */}
            </div>
          </div>
        </div>
        <div className="repostInfoArea">
          {source !== origin && (
              originAuthorDisplayName && (
                <div className="repostInfo">
                  <b>
                <span>Reposted from {originAuthorDisplayName}@{originAuthorHost}</span></b>
                </div>
              )
          )}
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
                            fullHost={host}
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