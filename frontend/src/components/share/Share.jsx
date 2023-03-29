import "./share.css";

import axios from "axios";
import { v4 as uuidv4 } from 'uuid';

import { useState } from "react";
import Dropdown from 'react-dropdown';

import useGetAuthorData from "../../useGetAuthorData";
import useGetTokens from "../../useGetTokens";

import PhotoSizeSelectActualOutlinedIcon from '@mui/icons-material/PhotoSizeSelectActualOutlined';
import { Switch, Button } from "@mui/material";

import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';

function Share (props) {
    const {setPostsUpdated} = props;
    const [files, setFiles] = useState([]);
    const [contentText, setContent] = useState("");
    const [message, setMessage] = useState();
    const [isPrivate, setIsPrivate] = useState(false); 
    const contentOptions = [
        { value: 'text/plain', label: 'Plaintext' },
        { value: 'text/markdown', label: 'Markdown' },
    ];
    const [contentType, setContentType] = useState(contentOptions[0].value);

    const [imageFile, setImageFile] = useState(null);
    const [imageBase64, setImageBase64] = useState(null);
    
    const {authorData, loading, authorError, authorID} = useGetAuthorData();
    const {tokens, tokenError} = useGetTokens();

    // change contentType
    function handleContentTypeChange(option) {
        setContentType(option.value);
    }

    // updating content text
    const handleTextChange = event => {
        setContent(event.target.value);
    };

    // select image from browser NEW!
    const handleFileUpload = (event) => {
        setImageFile(event.target.files[0]);
        const reader = new FileReader();
        reader.onloadend = () => {
            setImageBase64(reader.result);
        };
        reader.readAsDataURL(event.target.files[0]);
    };

    // delete image
    const handleDeleteImage = () => {
        setImageFile(null)
        setImageBase64(null);
    }

    // get followers to send a public post
    async function getFollowers() {
        const response = await axios.get(`/authors/${authorID}/followers`, {
            headers:{
                "Authorization": tokens[window.location.hostname]
            }
        });
        return response.data.items.map(obj => [obj.id+"/inbox/", new URL(obj.host).hostname]);
    }

    const sendImagePost = async() => {
        console.log(imageBase64);  // content
        console.log(imageFile.type)  // contentType
        // visibility: "unlisted"
    }

    const sendPost = async() => {
        // console.log("tt", tokens);
        // console.log("ttttt", tokens[authorData.host]);
        const p = axios
        .post(`/authors/${authorID}/inbox/`, {
            "type": "post",
            "id": `${authorData.host}/authors/${authorID}/posts/${uuidv4()}`,
            "contentType": contentType,
            "content": contentText,
            "author": authorData,
        },
        {
            headers: {
                "Authorization": tokens[window.location.hostname]
            }
        })
        
        const p2 = p.then((response) => {
            setPostsUpdated(response.data);
            setContent("");
            handleDeleteImage();
            const p3 = getFollowers()
            const p4 = p3.then((response2) => {
                const requestPromises = response2.map(obj => {
                    axios.post(obj[0], response.data, {
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
        <div className="share">

            <div className="shareCard">
            
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
                                    <b> Upload a Photo</b>
                                </div>
                            </label>
                        </div>

                        <div className="isPrivateSwitch">
                            <Switch
                                private={isPrivate}
                                onChange={(event) => setIsPrivate(event.target.checked)}
                                color="primary"
                            />
                            <b>Private</b>  
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
                                    {/* TODO: if it's an image post, then you actually have to call both 
                                    sendPost and sendImagePost.. maybe do a conditional inside sendPost? 
                                    or call sendImagePost, and then call sendPost inside sendImagePost */}
                                Post
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Share;