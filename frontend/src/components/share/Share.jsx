import "./share.css";
import { useState } from "react";
import CreateOutlinedIcon from '@mui/icons-material/CreateOutlined';
import PhotoSizeSelectActualOutlinedIcon from '@mui/icons-material/PhotoSizeSelectActualOutlined';
import { Switch } from "@mui/material";
import axios from "axios";
import useGetAuthorData from "../../useGetAuthorData";
import { v4 as uuidv4 } from 'uuid';

const Share = () => {

    const [files, setFiles] = useState([]);
    const [content, setContent] = useState("");
    const [message, setMessage] = useState();
    const [isPrivate, setIsPrivate] = useState(false); 
    const [contentType, setContentType] = useState("text/plain");  // TODO: figure out markdown, then images
    // const [fileURL, setFileURL] = useState(null)


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

    // const getFollowers = async () => {
    //     return axios
    //         .get(`/authors/${authorID}/followers`)
    //         // .then((response) => console.log("FOLLOWERS", response.data.items.map(obj => obj.id)))
    //         .then((response) => {
    //             return response.data.items.map(obj => obj.id);
    //             // return response
    //         })
    //         .catch((error) => console.log(error))
    // }

    async function getFollowers() {
        const response = await axios.get(`/authors/${authorID}/followers`);
        return response.data.items.map(obj => obj.id+"/inbox/");
    }

    // const data = {msg: "hello"};
    // const endpoints = ['http://localhost:8000/1/inbox', 'http://localhost:8000/2/inbox', 'http://localhost:8000/3/inbox'];

    // const promises = endpoints.map(endpoint => {
    // return axios.post(endpoint, data);
    // });

    // Promise.all(promises)
    // .then(responses => {
    //     console.log(responses);
    // })
    // .catch(error => {
    //     console.error(error);
    // });

    const sendPost = async(event) => {
        event.preventDefault();
        const p = axios
        .post(`/authors/${authorID}/inbox/`, {
            "type": "post",
            "title": "dasd I123123 Come",
            "id": `http://localhost:8000/authors/${authorID}/posts/${uuidv4()}`,
            "contentType": contentType,
            "content": content,
            "author": data,
        })
        
        const p2 = p.then((response) => {
            const p3 = getFollowers()
            const p4 = p3.then((response2) => {
                console.log("p3", p3)
                console.log("r2", response2)
                console.log("rd", response.data)
                const requestPromises = response2.map(endpoint => {
                axios.post(endpoint, response.data)
                })
                Promise.all(requestPromises)
                .then((responses) => {
                    console.log('All requests sent successfully:', responses);
                })
                .catch((error) => {
                    console.error('Error sending requests:', error);
                });
            }
            )
        })
        // axios
        //     .post(`/authors/${authorID}/inbox/`, {
        //         "type": "post",
        //         "title": "dasd I123123 Come",
        //         "id": `http://localhost:8000/authors/${authorID}/posts/${uuidv4()}`,
        //         "contentType": contentType,
        //         "content": content,
        //         "author": data,
        //     })
        //     .then((response) => {
        //         console.log("Sending to inbox...", response);
        //         // getFollowers();
        //         console.log("f", getFollowers())
        //         const requestPromises = getFollowers().map(endpoint => {
        //             axios.post(endpoint, response.data)
        //         })
        //         Promise.all(requestPromises)
        //         .then((responses) => {
        //             console.log('All requests sent successfully:', responses);
        //         })
        //         .catch((error) => {
        //             console.error('Error sending requests:', error);
        //         });
        //     })
        //     .catch((error) => console.log(error))
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