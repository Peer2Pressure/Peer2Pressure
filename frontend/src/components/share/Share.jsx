import "./share.css";

import axios from "axios";
import { v4 as uuidv4 } from 'uuid';

import { useState } from "react";

import PhotoSizeSelectActualOutlinedIcon from '@mui/icons-material/PhotoSizeSelectActualOutlined';
import { Button, Modal, Box } from "@mui/material";

import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';


function Share (props) {
    const { authorData, authorID, tokens } = props;
    const [contentText, setContent] = useState("");
    const [titleText, setTitle] = useState("");
    const [selectedUser, setSelectedUser] = useState(null);
    const visibilityOptions = [
        { value: 'PUBLIC', label: 'Public' },
        { value: 'FRIENDS', label: 'Friends' },
        { value: 'UNLISTED', label: 'Unlisted'},
        { value: 'PRIVATE', label: 'Select Friend' }
    ];
    const [visibility, setVisibility] = useState(visibilityOptions[0].value);
    const [isUnlisted, setIsUnlisted] = useState(false);
    const contentOptions = [
        { value: 'text/plain', label: 'Plaintext' },
        { value: 'text/markdown', label: 'Markdown' },
    ];
    const [contentType, setContentType] = useState(contentOptions[0].value);

    const [imageFile, setImageFile] = useState(null);
    const [imageBase64, setImageBase64] = useState(null);
    const [imageID, setImageID] = useState(null);

    const [connectionsModalOpen, setConnectionsModalOpen] = useState(false);
    const [connections, setConnections] = useState([]);

    // change visibility
    function handleVisibilityChange(option) {
        setVisibility(option.value);
        if (option.value === "PRIVATE") {
            handleConnectionsModalOpen();
        } else if (option.value === "UNLISTED") {
            setIsUnlisted(true);
            setVisibility("PUBLIC");  // unlisted posts are public if you know the URL
        } else {
            setSelectedUser(null);
            handleConnectionsModalClose();
            setIsUnlisted(false);
        }
    }

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
                console.log("FOLLOWERS", response.data.items);
            }   
        } catch (err) {
            console.log("Error getting followers: ", err);
        }
    };

    const handleConnectionsModalClose = () => {
        setConnectionsModalOpen(false);
        if (selectedUser !== null) {
            setVisibility(visibilityOptions[0].value);
        }
    };

    // change selected user
    const handleSelectUser = (user) => {
        setSelectedUser(user);
        handleConnectionsModalClose();
    };

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
    // select image from browser NEW!
    const handleFileUpload = (event) => {
        const imageUUID = uuidv4();
        setImageID(`${authorData.id}/posts/${imageUUID}`)
        setImageFile(event.target.files[0]);
        const reader = new FileReader();
        reader.onloadend = () => {
            setImageBase64(reader.result);
        };
        reader.readAsDataURL(event.target.files[0]);
    };

    // delete image
    const handleDeleteImage = () => {
        setImageFile(null);
        setImageBase64(null);
        setImageID("");
    }

    // get followers to send a post
    async function getFollowers() {
        const response = await axios.get(`/authors/${authorID}/followers/`, {
            headers:{
                "Authorization": tokens[window.location.hostname]
            }
        });
        if (selectedUser) {  
            console.log("working")
            return [[selectedUser.id.replace(/\/$/, "") +"/inbox/", new URL(selectedUser.host).hostname]];
        } else {
            return response.data.items.map(obj => [obj.id.replace(/\/$/, "") +"/inbox/", new URL(obj.host).hostname]);
        }
    }

    const sendImagePost = async() => {        
        axios
        .post(`/authors/${authorID}/inbox/`, {
            "type": "post",
            "id": `${imageID}`,
            "source": `${imageID}`,
            "origin": `${imageID}`,
            "title": titleText,
            "contentType": imageFile.type + ";base64",
            "content": imageBase64,
            "author": authorData,
            "unlisted": true,
            "visibility": visibility
        },
        {
            headers: {
                "Authorization": tokens[window.location.hostname]
            }
        })
        .catch((error) => {
            console.log("Error sending image post to current author's inbox: ", error)
        })
        .then((res) => {
            sendPost();
        })
    }

    const sendPost = async () => {
        const postUUID = uuidv4();
        const data = {
            "type": "post",
            "id": `${authorData.id}/posts/${postUUID}`,
            "source": `${authorData.id}/posts/${postUUID}`,
            "origin": `${authorData.id}/posts/${postUUID}`,
            "title": titleText,
            "contentType": imageID ?  "text/markdown" : contentType,
            "content": imageID ? contentText + `\n\n \n\n![](${imageID}/image)` : contentText,
            "author": authorData,
            "unlisted": isUnlisted,
            "visibility": visibility
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
            handleDeleteImage();
            setContent("");
            setTitle("");
            setVisibility("PUBLIC");
            setSelectedUser(null);
            handleDeleteImage();
            const p3 = getFollowers()
            const p4 = p3.then((response2) => {
                console.log("p3", p3);
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

                console.log(team12Data);
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
        <div className="share">

            <div className="shareCard">
                {/* write title of post */}
                <div className="titleBox">
                    <div className="titleField">
                        <input
                            name="title"
                            placeholder={"Add a title..."}
                            value={titleText}
                            onChange={handleTitleChange}
                        />
                    </div>
                </div>
            
                <div className="top">
                    {/* write content of post */}
                    <div className="textBox">
                        <textarea 
                            name="text" 
                            placeholder={"Write something..."}
                            value={contentText}
                            onChange={handleTextChange}
                        />
                    </div>
                </div>

                <div className="imgPreviewBox">
                    {/* show the image in a preview box */}
                    <div className="imgPreview">
                        {imageBase64 && (
                            <div className="imgContainer">
                                <img src={imageBase64} alt="Image Preview" />
                                <button onClick={handleDeleteImage}>x</button>
                            </div>
                        )}
                    </div>
                </div>

                <div className="dmInfo">
                    <div className="dmInfoText">
                        {selectedUser && (
                            <div className="dmInfoTextContainer">
                                <p>Direct Message to <i>{selectedUser.displayName}</i></p>
                            </div>
                        )}
                    </div>
                </div>

                <div className="bottom">
                    <div className="postOptionsContainer">
                        {/* actual image choice */}
                        <div className="shareImage">                    
                            <input 
                                type="file"
                                id="file" 
                                accept="image/png, image/jpeg"
                                style={{display:"none"}} 
                                onChange={handleFileUpload}
                            />
                            <label htmlFor="file">
                                <div className="uploadImg">
                                    <PhotoSizeSelectActualOutlinedIcon 
                                        fontSize="small"     
                                        color="primary"
                                    />
                                    <b> Upload Photo</b>
                                </div>
                            </label>
                        </div>

                        <div className="chooseVisibility">
                            <Dropdown 
                                options={visibilityOptions}
                                value={visibility}
                                onChange={handleVisibilityChange}
                            />
                        </div>
                        <div className="chooseContentType">
                            <Dropdown 
                                options={contentOptions}
                                value={contentType}
                                onChange={handleContentTypeChange}
                            />
                        </div>
                    </div>
                    
                    <div className="postButtonContainer">
                        <div className="postButtonBox">
                            <Button 
                                sx={{borderRadius: 20}} 
                                variant="contained" 
                                className="postButton" 
                                role="button" 
                                onClick={imageBase64 ? sendImagePost : sendPost}>
                                Post
                            </Button>
                        </div>
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
                    <h2 id="connections-modal-title" style={{ color: '#0058A2' }}>Select Friend</h2>
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
                                    onClick={() => handleSelectUser(connection)}
                                >
                                    Select
                                </button>
                            </li>
                        ))}
                    </ul>
                </Box>
            </Modal>
        </div>
    );
};

export default Share;