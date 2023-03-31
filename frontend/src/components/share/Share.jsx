import "./share.css";
import { useState } from "react";
import PhotoSizeSelectActualOutlinedIcon from '@mui/icons-material/PhotoSizeSelectActualOutlined';
import { Switch } from "@mui/material";
import axios from "axios";
import useGetAuthorData from "../../useGetAuthorData";
import { v4 as uuidv4 } from 'uuid';
import useGetTokens from "../../useGetTokens";
import Button from "@mui/material/Button";
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
    const [hasImage, setHasImage] = useState(false);
    const [imageBase64, setImageBase64] = useState(null);
    const [postImage, setPostImage] = useState({
        myFile: "",
    });
    

    const {authorData, loading, authorError, authorID} = useGetAuthorData();
    const {tokens, tokenError} = useGetTokens();

    function handleContentTypeChange(option) {
        setContentType(option.value);
    }

    const handleTextChange = event => {
        setContent(event.target.value);
    };

    const convertToBase64 = (file) => {
        return new Promise((resolve, reject) => {
            const fileReader = new FileReader();
            fileReader.readAsDataURL(file);
            fileReader.onload = () => {
                resolve(fileReader.result);
            };
            fileReader.onerror = (error) => {
                reject(error);
            };
        });
    };

    const handleFile = async (e) => {
        setMessage("");
        setHasImage(true);
        // const file = e.target.files[0];
        let file = e.target.files;
        for (let i=0; i<file.length; i++) {

        
        // const fileType = file['type'];
        // const validImageTypes = ['image/jpeg', 'image/png'];
        // if (validImageTypes.includes(fileType)) {
            const base64 = await convertToBase64(file[i]);
            setPostImage({ ...postImage, myFile: base64 });
        // } else {
            // setMessage("only jpeg and png accepted");
        // }
    }
      };

    // const handleFile = (e) => {
    //     setMessage("");
    //     setHasImage(true);
    //     let file = e.target.files;
        
    //     for (let i = 0; i < file.length; i++) {
    //         const fileType = file[i]['type'];
    //         const validImageTypes = ['image/jpeg', 'image/png'];
    //         if (validImageTypes.includes(fileType)) {
    //             setFiles([...files,file[i]]);
    //         } else {
    //             setMessage("only jpeg and png accepted");
    //         }
    //     }
    // };

    const removeImage = (i) => {
        setFiles(files.filter(x => x.name !== i));
        setHasImage(false);
    } 

    async function getFollowers() {
        const response = await axios.get(`/authors/${authorID}/followers/`, {
            headers:{
                "Authorization": tokens[window.location.hostname]
            }
        });
        return response.data.items.map(obj => [obj.id+"/inbox/", new URL(obj.host).hostname]);
    }

    const sendPost = async(event) => {
        // console.log("author_data123: ", authorData, authorID);
        // console.log("tt", tokens);
        // console.log("ttttt", tokens[authorData.host]);
        const uuid = uuidv4()
        event.preventDefault();
        const p = axios
        .post(`/authors/${authorID}/inbox/`, {
            "type": "post",
            "id": `${authorData.id}/posts/${uuid}`,
            "source": `${authorData.id}/posts/${uuid}`,
            "origin": `${authorData.id}/posts/${uuid}`,
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
                            value={contentText}
                            onChange={handleTextChange}
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
                                    />
                                    <b> Upload a Photo</b>
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
                            <Button sx={{borderRadius: 20}} variant="contained" className="postButton" role="button" onClick={sendPost}>Post</Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Share;