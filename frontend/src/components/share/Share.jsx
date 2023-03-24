import "./share.css";
import { useState } from "react";
import CreateOutlinedIcon from '@mui/icons-material/CreateOutlined';
import PhotoSizeSelectActualOutlinedIcon from '@mui/icons-material/PhotoSizeSelectActualOutlined';
import { Switch } from "@mui/material";
import axios from "axios";
import useGetAuthorData from "../../useGetAuthorData";

const Share = () => {

    const [files, setFiles] = useState([]);
    const [content, setContent] = useState("");
    const [message, setMessage] = useState();
    const [isPrivate, setIsPrivate] = useState(false); 
    // const [fileURL, setFileURL] = useState(null)

    // const [authorId, loading, error] = useGetAuthorID();
    // const authorId = "596f24c4-430b-4546-98d2-1f83995259e8"

    const {data, loading, error, authorID} = useGetAuthorData();

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

    const sendPost = async(event) => {
        event.preventDefault();
        axios
        .post(`/authors/${authorID}/inbox/`, {
            // "type": "post",
            // "title": "dasd I123123 Come",
            // "id": `/authors/${authorID}/posts/5276b41d-8894-4aaf-9dc9-c2e210ed4bd2`,
            // "source": "",
            // "origin": "",
            // "description": "",
            // "contentType": "text/plain",
            // "content": content,
            // "author": data,
            // "published": "2023-03-24T00:47:20.400082Z",
            // "visibility": "PUBLIC",
            // "unlisted": false
        })
        .then((response) => console.log(response))
        .catch((error) => console.log(error))
        // .post(`/authors/${authorId}/posts/`, {
        //     "content": content,
        //     "contentType": "text/plain"
        // })
    //     // .then((response) => console.log(response.data.id))
    //     .then(async (response) => {
    //         const response_1 = await axios
    //             .post(`/authors/${authorId}/inbox/`, {
    //                 "type": response.data.type,
    //                 "title": response.data.title,
    //                 "id": response.data.id,
    //                 "source": response.data.source,
    //                 "origin": response.data.origin,
    //                 "description": response.data.description,
    //                 "contentType": response.data.contentType,
    //                 "content": response.data.content,
    //                 "author": response.data.author,
    //                 "published": response.data.published,
    //                 "visibility": response.data.visibility,
    //                 "unlisted": response.data.unlisted
    //             });
    //         return console.log(response_1);
    //     })
    //     .catch(error => console.log(error));
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
                    {/* <div className="shareText">
                        <CreateOutlinedIcon 
                            fontSize="small" 
                            color="primary"
                        /> <b>Create a Post</b>
                    </div> */}
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