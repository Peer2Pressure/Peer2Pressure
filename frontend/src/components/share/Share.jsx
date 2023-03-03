import "./share.css";
import { useState } from "react";
import CreateOutlinedIcon from '@mui/icons-material/CreateOutlined';
import PhotoSizeSelectActualOutlinedIcon from '@mui/icons-material/PhotoSizeSelectActualOutlined';
import { Switch } from "@mui/material";
import axios from "axios";


const Share = () => {

    const [files, setFiles] = useState([]);
    const [content, setContent] = useState("");
    const [message, setMessage] = useState();
    const [isPrivate, setIsPrivate] = useState(false); 
    // const [fileURL, setFileURL] = useState(null)

    const authorId = "cfa35fee-0696-4253-91c0-df7646cde2fe";

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
        .post("http://localhost:8000/authors/" + authorId + "/posts/", {
            "content": content,
            "author" : authorId,
            "is_private": false,
            "image": files  // or test with null
        })
        .then(response => console.log('Posting data', response))
        .catch(error => console.log(error));
        // .catch(console.log(files));
    }

    return (
        <div className="share">
            <div className="shareCard">
                <div className="top">
                    <div className="shareText">
                        <CreateOutlinedIcon 
                            fontSize="small" 
                            color="primary"
                        /> <b>Create a Post</b>
                    </div>
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
                                /> <b>Upload a Photo</b>
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

                <div className="bottom">
                    <div className="textBox">
                        <textarea 
                            name="text" 
                            placeholder={"Write something..."}
                            value={content}
                            onChange={handleContentChange}
                        />   
                    </div>
                       
                    <div className="imgPreview">
                        <span className="errorMsg">{message}</span>
                        {files.map((file, key) => {
                            return (
                                <div key={key} className="imgContainer">
                                    <button onClick={() => { removeImage(file.name)}}>x</button>
                                    <img src={URL.createObjectURL(file)}/>
                                </div>
                            )
                        })}
                    </div>

                </div>
                <div className="buttonBox">
                    <button className="postButton" onClick={sendPost}>Post</button>
                </div>
            </div>
        </div>
    );
};

export default Share;