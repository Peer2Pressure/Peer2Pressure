import "./editPost.css";

import axios from "axios";
import { v4 as uuidv4 } from 'uuid';

import { forwardRef, useState } from "react";

import useGetAuthorData from "../../useGetAuthorData";
import useGetTokens from "../../useGetTokens";

import PhotoSizeSelectActualOutlinedIcon from '@mui/icons-material/PhotoSizeSelectActualOutlined';
import { Switch, Button } from "@mui/material";

import ReactMarkdown from 'react-markdown'
import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';


const EditPost = forwardRef(
    ({ postID, postTitle, postText, postContentType, postAuthorID, onClose }, ref) => {
    const [contentText, setContent] = useState(postText);
    const [titleText, setTitle] = useState(postTitle);
    const visibilityOptions = [
        { value: 'PUBLIC', label: 'Public' },
        { value: 'FRIENDS', label: 'Friends' }
    ];
    const [visibility, setVisibility] = useState(visibilityOptions[0].value);
    const contentOptions = [
        { value: 'text/plain', label: 'Plaintext' },
        { value: 'text/markdown', label: 'Markdown' },
    ];
    const [contentType, setContentType] = useState(postContentType);
       
    const {authorData, loading, authorError, authorID} = useGetAuthorData();
    const {tokens, tokenError} = useGetTokens();

    // images are weird so markdown might be an ok compromise
    const regex = /!\[.*?\]\((.*?)\)/;
    const markdownImageMatch = regex.exec(contentText);
    const markdownImage = markdownImageMatch ? markdownImageMatch[0] : null;

    const handleClose = () => {
        if (onClose) {
            onClose();
        }
    };

    // change visibility
    function handleVisibilityChange(option) {
        setVisibility(option.value);
    }

    // change contentType
    function handleContentTypeChange(option) {
        setContentType(option.value);
    }

    // updating content text
    const handleTextChange = event => {
        setContent(event.target.value);
    };

    // updating title text
    const handleTitleChange = event => {
        setTitle(event.target.value);
    };

    // get followers to send a public post
    async function getFollowers() {
        const response = await axios.get(`/authors/${authorID}/followers/`, {
            headers:{
                "Authorization": tokens[window.location.hostname]
            }
        });
        return response.data.items.map(obj => [obj.id.replace(/\/$/, "") +"/inbox/", new URL(obj.host).hostname]);
    }

    const sendPost = async () => {
        const data = {
            "type": "post",
            "id": postID,
            "source": postID,
            "origin": postID,
            "title": titleText,
            "contentType": markdownImage ?  "text/markdown" : contentType,
            "content": contentText,
            "author": authorData,
        }

        console.log("DATA!", postID);

        const p1 = axios
        .post(postID+"/", data, {
            headers: {
                "Authorization": tokens[window.location.hostname]
            }
        })
        .catch((error) => {
            console.log(error)})
        
        const p2 = p1.then((response) => {
            setContent("");
            setTitle("");
            handleClose();
            const p3 = getFollowers()
            const p4 = p3.then((response2) => {
                
                //  Custom payload to post to Team 11 inbox
                const team11Data = {};
                team11Data["@context"] = "";
                team11Data["summary"] = "";
                team11Data["type"] = "post";
                team11Data["author"] = authorData;
                team11Data["object"] = response.data;
                
                const team12Data = {};
                team12Data["type"] = "post";
                team12Data["post"] = response.data;
                team12Data["sender"] = authorData;

                console.log(team11Data);

                const requestPromises = response2.map(obj => {
                    let payload = response.data;
                    if (obj[1] === "quickcomm-dev1.herokuapp.com") {
                        payload = team11Data;
                    } else if (obj[1] === "cmput404-project-data.herokuapp.com") {
                        payload = team12Data;
                    }
                    axios.post(obj[0], payload, {
                        maxRedirects: 3,
                        headers: {
                            "Authorization": tokens[obj[1]]
                        }
                    });
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
        <div className="share2" ref={ref}>

            <div className="shareCard2">
                {/* write title of post */}
                <div className="titleBox2">
                    <div className="titleField2">
                        <input
                            name="title"
                            placeholder={"Add a title..."}
                            value={titleText}
                            onChange={handleTitleChange}
                        />
                    </div>
                </div>
            
                <div className="top2">
                    {/* write content of post */}
                    <div className="textBox2">
                        <textarea 
                            name="text" 
                            placeholder={"Write something..."}
                            value={contentText}
                            onChange={handleTextChange}
                        />
                    </div>
                </div>

                <div className="imgPreviewBox2">
                    {/* show the image in a preview box */}
                    <div className="imgPreview2">
                        {contentType === "text/markdown" && (
                            <div className="markdownPreview">
                                <ReactMarkdown>{markdownImage}</ReactMarkdown>
                            </div>
                        )}
                    </div>
                </div>

                <div className="bottom2">
                    <div className="postOptionsContainer2">
                        <div className="chooseVisibility">
                                <Dropdown 
                                    options={visibilityOptions}
                                    value={visibility}
                                    onChange={handleVisibilityChange}
                                />
                            </div>
                        <div className="chooseContentType2">
                            <Dropdown 
                                options={contentOptions}
                                value={contentType}
                                onChange={handleContentTypeChange}
                            />
                        </div>
                    </div>
                    
                    <div className="postButtonContainer2">
                        <div className="postButtonBox2">
                            <Button 
                                sx={{borderRadius: 20}} 
                                variant="contained" 
                                className="postButton" 
                                role="button" 
                                onClick={sendPost}>
                                Post
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
);

export default EditPost;