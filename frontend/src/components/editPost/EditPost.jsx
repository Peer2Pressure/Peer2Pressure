import "./editPost.css";

import axios from "axios";
import { v4 as uuidv4 } from 'uuid';

import { forwardRef, useState } from "react";

import useGetAuthorData from "../../useGetAuthorData";
import useGetTokens from "../../useGetTokens";

import PhotoSizeSelectActualOutlinedIcon from '@mui/icons-material/PhotoSizeSelectActualOutlined';
import { Switch, Button } from "@mui/material";

import Dropdown from 'react-dropdown';
import 'react-dropdown/style.css';


const EditPost = forwardRef(
    ({ postID, postTitle, postText, postContentType, postAuthorID}, ref) => {
    // const {setPostsUpdated} = props;
    const [contentText, setContent] = useState(postText);
    const [titleText, setTitle] = useState(postTitle);
    // console.log(JSON.stringify(postTitle));
    const [isPrivate, setIsPrivate] = useState(false); 
    const contentOptions = [
        { value: 'text/plain', label: 'Plaintext' },
        { value: 'text/markdown', label: 'Markdown' },
    ];
    const [contentType, setContentType] = useState(postContentType);

    const [imageFile, setImageFile] = useState(null);
    const [imageBase64, setImageBase64] = useState(null);
    const [imageID, setImageID] = useState(null);
       
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

    // updating title text
    const handleTitleChange = event => {
        setTitle(event.target.value);
    };

    // select image from browser
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

    // get followers to send a public post
    async function getFollowers() {
        const response = await axios.get(`/authors/${authorID}/followers/`, {
            headers:{
                "Authorization": tokens[window.location.hostname]
            }
        });
        return response.data.items.map(obj => [obj.id.replace(/\/$/, "") +"/inbox/", new URL(obj.host).hostname]);
    }

    const sendImagePost = async() => {
        // const postUUID = uuidv4();
        sendPost();
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
            "visibility": "PUBLIC"
        },
        {
            headers: {
                "Authorization": tokens[window.location.hostname]
            }
        }).catch((error) => {
            console.log("Error sending image post to current author's inbox: ", error)
        });
        
        // Might not need to send to followers' inboxes
        
        // .then((response) => {
        //     const p3image = getFollowers()
        //     const p4image = p3image.then((response2) => {
        //         const requestPromises = response2.map(obj => {
        //             axios.post(obj[0], response.data, {
        //                 headers: {
        //                     "Authorization": tokens[obj[1]]
        //                 }
        //             });
        //         })
        //         Promise
        //         .all(requestPromises)
        //         .then((responses) => {
        //             console.log('All requests sent successfully:', responses);
        //         })
        //         .catch((error) => {
        //             console.error('Error sending requests:', error);
        //         })
        //     })
        // });
    }

    const sendPost = async () => {
        const postUUID = postID;
        const data = {
            "type": "post",
            // "id": `${authorData.id}/posts/${postUUID}`,
            "id": postID,
            "source": `${authorData.id}/posts/${postUUID}`,
            "origin": `${authorData.id}/posts/${postUUID}`,
            "title": titleText,
            "contentType": imageID ?  "text/markdown" : contentType,
            "content": imageID ? contentText + `\n\n \n\n![](${imageID}/image)` : contentText,
            "author": authorData,
        }

        console.log("DATA!", postID);
        console.log(postAuthorID);
        const p1 = axios
        // .post(`/authors/${authorID}/inbox/`, data, {
        .post(postID+"/", data, {
            headers: {
                "Authorization": tokens[window.location.hostname]
            }
        })
        .catch((error) => {
            console.log(error)})
        
        const p2 = p1.then((response) => {
            handleDeleteImage();
            // setPostsUpdated(response.data);
            setContent("");
            setTitle("");
            handleDeleteImage();
            const p3 = getFollowers()
            const p4 = p3.then((response2) => {
                
                //  Custom payload to post to Team 11 inbox
                const team11Data = {};
                team11Data["@context"] = "";
                team11Data["summary"] = "";
                team11Data["type"] = "post";
                team11Data["author"] = authorData;
                team11Data["object"] = response.data;
                
                console.log(team11Data);

                const requestPromises = response2.map(obj => {
                    axios.post(obj[0], obj[1] !== "quickcomm-dev1.herokuapp.com" ? response.data : team11Data, {
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
                        {imageBase64 && (
                            <div className="imgContainer2">
                                <img src={imageBase64} alt="Image Preview" />
                                <button onClick={handleDeleteImage}>x</button>
                            </div>
                        )}
                    </div>
                </div>

                <div className="bottom2">
                    <div className="postOptionsContainer2">
                        {/* actual image choice */}
                        {/* this works weird */}
                        {/* <div className="shareImage2">                    
                            <input 
                                type="file"
                                id="file" 
                                accept="image/png, image/jpeg"
                                style={{display:"none"}} 
                                onChange={handleFileUpload}
                            />
                            <label htmlFor="file">
                                <div className="uploadImg2">
                                    <PhotoSizeSelectActualOutlinedIcon 
                                        fontSize="small"     
                                        color="primary"
                                    />
                                    <b> Upload a Photo</b>
                                </div>
                            </label>
                        </div> */}

                        <div className="isPrivateSwitch2">
                            <Switch
                                private={isPrivate}
                                onChange={(event) => setIsPrivate(event.target.checked)}
                                color="primary"
                            />
                            <b>Private</b>  
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
                                // onClick={imageBase64 ? sendImagePost : sendPost}>
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