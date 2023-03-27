import { Avatar, Button, TextField } from "@mui/material";
import "./profileSetting.css";
import useFetch from "../../useFetch";
import axios from "axios";
import { useEffect, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
// import useGetAuthorID from "../../useGetAuthorID.js";
import useGetAuthorData from "../../useGetAuthorData";
import useGetFullAuthorID from "../../useGetFullAuthorID";

export default function ProfileSetting() {

    const navigate = useNavigate();
    const [userData, setUserData] = useState({
        id: '',
        // username: '',
        // title: '',
        displayName: '',
        // email: '',
        // password: '',
        profileImage: '',
        github: '',
    });
   
    const handleChange2 = (username, value) => {
        // if (value !== "") {
        setUserData({
            ...userData,
            [username] : value
        });
        // };
    };
    // grabbing data from /get_author_id/ and /authors/author_id APIs
    const {data, loading, error, authorID} = useGetAuthorData();
    // console.log(data.profileImage);
    // get current author ID (note: not UUID)
    // const [authorIDD, setAuthorIDD] = useState(null);
    const {authorIDD} = useGetFullAuthorID();

    // const [submitForm, setSubmitForm] = useState(false);

    // useEffect(() => {
    //     const getAuthorIDD = async () => {
    //         try {
    //             console.log("test123", authorID);
    //             const response = await axios.get("/authors/" + authorID + "/");
    //             setAuthorIDD(response.data.id);
                
    //             setIsDataReady(true);
    //         } catch(error) {
    //             setError2(error2);
    //         }
    //     };
    //     getAuthorIDD();
    // }, [authorID]);

    console.log("author UUID: ", authorID);
    console.log("author ID: ", authorIDD);



    const handleSubmit = (e) => {


        // if (authorID === null && authorIDD === null) {
        //     return;
        // }
        e.preventDefault();
        const formData = new FormData();
        // formData.append('username', userData.username || data?.username);
        // formData.append('email', userData.email || data?.email);
        // formData.append('password', userData.password || data?.password);
        formData.append('displayName', userData.name || data?.displayName);
        formData.append('github', userData.github || data?.github);
        formData.append('profileImage', userData.profileImage || data?.profileImage);
        formData.append('id', authorIDD);

        // console.log(userData.displayName);
        // if (userData.avatar) {
        //     formData.append('avatar', userData.avatar, userData.avatar.name);
        // }
    
        // console.log("usernameeeee: "+userData);
        // console.log("/authors/" + authorID + '/');
        console.log("FORM DATA: ", formData);
        axios
        .post(
            "/authors/"+ authorID + "/", 
            formData,
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            })
        .then((response) => {
            console.log(response.data);
            // window.location.reload();
        }).catch((error) => {
            console.log("HAHAHA")
            console.log("Error Response: ", error.response);
            console.log("Error Data: ", error.response.data)
        }).finally(() => {
            window.location.reload();
        })
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="profileSettingsBox">
                <div className="profileImageBox">
                    <Avatar src={data?.profileImage} sx={{width:100, height:100}}/>
                    {/* <input type="file" accept="image/*" onChange={handleFileChange}/> */}
                    {/* <label htmlFor="avatar-input">
                        <Button component="span">Change image</Button>
                    </label> */}
                </div>
                <div className="profileDetailsBox">
                    {/* <div className="usernameBox">
                        <h2 class="fieldTitle">Username</h2>
                        
                        <TextField label="username" placeholder={data?.username} value={userData.username} onChange={(e) => handleChange2("username", e.target.value)}/>
                    </div> */}
                    <div className="avatarBox">
                        <h2 className="fieldTitle">Profile Avatar</h2>
                        <TextField label="Avatar Link" placeholder={data?.profileImage} value={userData.profileImage} onChange={(e) => handleChange2("profileImage", e.target.value)} />
                    </div>
                    <div className="fullNameBox">
                        <h2 className="fieldTitle">Full Name</h2>
                        <TextField label="Name" placeholder={data?.displayName} value={userData.name} onChange={(e) => handleChange2("name", e.target.value)} />
                        {/* <TextField label="First Name" placeholder={data??.displayName} />
                        <TextField label="Last Name" placeholder={data??.type} /> */}
                    </div>
                    <div className="gitHubBox">
                        <h2 className="fieldTitle">GitHub</h2>
                        <TextField label="GitHub Profile ID" placeholder={data?.github} value={userData.github} onChange={(e) => handleChange2("github", e.target.value)} />
                    </div>
                    {/* <div className="emailBox">
                        <h2 className="fieldTitle">Email</h2>
                        <TextField label="abc@email.com" placeholder={data?.email} defaultValue={userData.email} onChange={(e) => handleChange2("email", e.target.value)}/>
    
                    </div> */}
                    {/* <div className="passwordBox">
                        <h2 className="fieldTitle">Password</h2>
                        <TextField type="password" placeholder="********" defaultValue={userData.password} onChange={(e) => handleChange2("password", e.target.value)}/>
                    </div> */}
                </div>  
                <div className="buttonBox">
                    <Button variant="outlined" onClick={()=>{navigate(-1)}}>Cancel</Button>
                    <Button type='submit' variant="contained" onClick={handleSubmit}>Save</Button>
                    {/* onClick={() => setButtonClicked(!buttonClicked)} */}
                    {/* disabled={authorID === null && authorIDD === null} */}
                </div>
                </div>
        </form>
      )
}
