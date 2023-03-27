import "./share.css";
import { useState } from "react";
import PhotoSizeSelectActualOutlinedIcon from '@mui/icons-material/PhotoSizeSelectActualOutlined';
import { Switch } from "@mui/material";
import axios from "axios";
import useGetAuthorData from "../../useGetAuthorData";
import { v4 as uuidv4 } from 'uuid';
import useGetTokens from "../../useGetTokens";

function Share(props) {
    const {setPostsUpdated} = props;
    const [files, setFiles] = useState([]);
    const [content, setContent] = useState("");
    const [message, setMessage] = useState();
    const [isPrivate, setIsPrivate] = useState(false); 
    const [contentType, setContentType] = useState("text/plain");  // TODO: figure out markdown, then images
    // const [fileURL, setFileURL] = useState(null)

    const {authorData, loading, authorError, authorID} = useGetAuthorData();
    const {tokens, tokenError} = useGetTokens();

    const handleContentChange = event => {
        setContent(event.target.value);
      };

    const handleFile = (e) => {
        setMessage("");
        let file = e.target.files;
        
        for (let i = 0; i < file.length; i++) {
            const fileType = file[i]['type'];
            const validImageTypes = ['image/jpeg', 'image/png'];
            if (validImageTypes.includes(fileType)) {
                setFiles([...files,file[i]]);
            } else {
                setMessage("only jpeg and png accepted");
            }
        }
    };

    const removeImage = (i) => {
        setFiles(files.filter(x => x.name !== i));
    } 

    async function getFollowers() {
        const response = await axios.get(`/authors/${authorID}/followers`, {
            headers:{
                // "Authorization": tokens[window.location.origin]
                "Authorization": tokens[authorData.host]
            }
        });
        return response.data.items.map(obj => [obj.id+"/inbox/", obj.host+"/"]);
    }

    const sendPost = async(event) => {
        // console.log("author_data123: ", authorData, authorID);
        console.log("tt", tokens);
        console.log("ttttt", tokens[authorData.host]);
        event.preventDefault();
        const p = axios
        .post(`/authors/${authorID}/inbox/`, {
            "type": "post",
            "id": `${authorData.host}/authors/${authorID}/posts/${uuidv4()}`,
            "contentType": contentType,
            "content": content,
            "author": authorData,
        },
        {
            headers: {
                // "Authorization": tokens[window.location.origin]
                "Authorization": tokens[authorData.host]
            }
        })
        
        const p2 = p.then((response) => {
            setPostsUpdated(response.data);
            setContent("");
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
                .finally(() => {
                    console.log("empty text area")
                })
            }
            )
        })
    }

    return (
        <div className="share">
            <div className="shareCard">
                

                <div className="top">
                    <div className="textBox">
                        <textarea 
                            name="text" 
                            placeholder={"Write something..."}
                            value={content}
                            onChange={handleContentChange}
                        />
                          
                    </div>
                       
                    <div className="imgPreview" role="test">
                        <span className="errorMsg">{message}</span>
                        {files.map((file, key) => {
                            return (
                                <div key={key} className="imgContainer">
                                    <button onClick={() => { removeImage(file.name)}}>x</button>
                                    <img src={URL.createObjectURL(file)} alt={file}/>   
                                    {/* alt for tests, idk what file actually is though */}
                                </div>
                            )
                        })}
                    </div>

                </div>
                <div className="bottom">
                    <div className="postOptionsContainer">
                        <div className="shareImage">
                            <input 
                                type="file"
                                id="file" 
                                style={{display:"none"}} 
                                onChange={handleFile}
                            />
                            <label htmlFor="file">
                                <div className="uploadImg">
                                    <PhotoSizeSelectActualOutlinedIcon 
                                        fontSize="small"     
                                        color="primary"
                                    /> <b> Upload a Photo</b>
                                    <img src = {Image} alt="" /> 
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
                    </div>
                    <div className="postButtonContainer">
                        <div className="postButtonBox">
                            <button className="postButton" role="button" onClick={sendPost}>Post</button>
                        </div>
                    </div>
                    
                </div>
                
            </div>
        </div>
    );
};

export default Share;