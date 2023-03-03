import "./share.css";
import { useState } from "react";
import CreateOutlinedIcon from '@mui/icons-material/CreateOutlined';
import PhotoSizeSelectActualOutlinedIcon from '@mui/icons-material/PhotoSizeSelectActualOutlined';
import { Switch } from "@mui/material";
import axios from "axios";


const Share = () => {


    const [files, setFile] = useState([]);
    const [desc, setDesc] = useState("");
    const [message, setMessage] = useState();
    const [isPrivate, setIsPrivate] = useState(false); 
    const authorId = "7156bb35-4e95-4911-a6f6-ef9bdc77da75";

    const handleFile = (e) => {
        setMessage("");
        let file = e.target.files;
        
        for (let i = 0; i < file.length; i++) {
            const fileType = file[i]['type'];
            const validImageTypes = ['image/jpeg', 'image/png'];
            if (validImageTypes.includes(fileType)) {
                setFile([...files,file[i]]);
            } else {
                setMessage("only images accepted");
            } 
        }
    }; 

    const removeImage = (i) => {
       setFile(files.filter(x => x.name !== i));
    }

    const sendPost = async(event) => {
        event.preventDefault();
        axios
        .post("http://localhost:8000/authors/" + authorId + "/posts/", {
            "content": "okay it worked!",
            "author" : authorId,
            "is_private": false,
        })
        .then(response => console.log('Posting data', response))
        .catch(error => console.log(error));
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
                        <textarea name="text" placeholder={"Write something..."} />   
                    </div>
                       
                    <div className="imgPreview">
                        <span className="errorMsg">{message}</span>
                        {files.map((file, key) => {
                            return (
                                <div key={key}>
                                    <i onClick={() => { removeImage(file.name)}}></i>            
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