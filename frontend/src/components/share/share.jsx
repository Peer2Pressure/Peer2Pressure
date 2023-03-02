import "./share.css";
import { useState } from "react";
import CreateOutlinedIcon from '@mui/icons-material/CreateOutlined';
import PhotoSizeSelectActualOutlinedIcon from '@mui/icons-material/PhotoSizeSelectActualOutlined';


const Share = () => {


    const [files, setFile] = useState([]);
    const [desc, setDesc] = useState("");
    const [message, setMessage] = useState();

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

    const handleClick = async(event) => {
        event.preventDefault()
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
                </div>
                
                

                <div className="bottom">
                    <textarea name="text" placeholder={"Write something..."} />                    

                    <div classname="imgPreview">
                        <span classname="errorMsg">{message}</span>
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
                
                <button className="postButton" onClick={handleClick}>Post</button>
            </div>
        </div>
    );
};

export default Share;