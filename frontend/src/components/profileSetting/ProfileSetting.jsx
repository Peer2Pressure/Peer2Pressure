import { Avatar, Button, TextField } from "@mui/material";
import "./profileSetting.css";
import useFetch from "../../useFetch";
import axios from "axios";
import { useEffect, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import useGetAuthorID from "../../useGetAuthorID.js"
import useGetAuthorData from "../../useGetAuthorData";



export default function ProfileSetting() {
    
    // grabbing data from /get_author_id/ and /authors/author_id APIs
    const {data, loading1, error1, authorID} = useGetAuthorData();

    const navigate = useNavigate();
    const [userData, setUserData] = useState({
        username: '',
        title: '',
        name: '',
        email: '',
        password: '',
        avatar: null
    });
    // if (loading1) return <h1>Loading...</h1>;
    // if (error1) console.log(error1);
    const handleFileChange = (event) => {
        setUserData({
            ...userData,
            avatar: event.target.files[0]
        });
        console.log("EVENT  :   ", event.target.files);
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append('username', userData.username || data?.username);
        formData.append('email', userData.email || data?.email);
        formData.append('password', userData.password || data?.password);
        formData.append('name', userData.name || data?.name);
        if (userData.avatar) {
            formData.append('avatar', userData.avatar, userData.avatar.name);
        }
    
        console.log("usernameeeee: "+userData);
        // console.log("/authors/" + authorID + '/');
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
            window.location.reload();
        }).catch((error) => {
            console.log(error);
        });
    };

    // const handleChange = (event) => {
    //     setUserData({
    //         ...userData,
    //         [event.target.name]: event.target.value,
    //     });
    // };

    const handleChange2 = (username, value) => {
        if (value !== "") {
            setUserData({
                ...userData,
                [username] : value
            });
        };
    };

    // // console.log("forData: "+formData);
    // console.log("username: "+userData.username);
    // console.log("email: " + userData.email);    
    // console.log('name: '+userData.name);

    return (
        <form onSubmit={handleSubmit}>
            <div className="profileSettingsBox">
                <div className="profileImageBox">
                    <Avatar src={data?.profileImage} sx={{width:100, height:100}}/>
                    <input type="file" accept="image/*" onChange={handleFileChange}/>
                    {/* <label htmlFor="avatar-input">
                        <Button component="span">Change image</Button>
                    </label> */}
                </div>
                <div className="profileDetailsBox">
                    <div className="usernameBox">
                        <h2 class="fieldTitle">Username</h2>
                        {/* <TextField label="username" placeholder={data?.username} value={userData.username} onChange={handleChange}/> */}
                        <TextField label="username" placeholder={data?.username} value={userData.username} onChange={(e) => handleChange2("username", e.target.value)}/>
                    </div>
                    <div className="fullNameBox">
                        <h2 className="fieldTitle">Full Name</h2>
                        <TextField label="Name" placeholder={data?.name} value={userData.name} onChange={(e) => handleChange2("name", e.target.value)} />
                        {/* <TextField label="First Name" placeholder={data??.displayName} />
                        <TextField label="Last Name" placeholder={data??.type} /> */}
                    </div>
                    <div className="emailBox">
                        <h2 className="fieldTitle">Email</h2>
                        <TextField label="abc@email.com" placeholder={data?.email} defaultValue={userData.email} onChange={(e) => handleChange2("email", e.target.value)}/>
                        {/* <TextField label="abc@email.com" placeholder={data??.email}/> */}
    
                    </div>
                    <div className="passwordBox">
                        <h2 className="fieldTitle">Password</h2>
                        <TextField type="password" placeholder="********" defaultValue={userData.password} onChange={(e) => handleChange2("password", e.target.value)}/>
                        {/* <TextField type="password" placeholder="********"/> */}
                    </div>
                </div>  
                <div className="buttonBox">
                    <Button variant="outlined" onClick={()=>{navigate(-1)}}>Cancel</Button>
                    <Button variant="contained" onClick={handleSubmit}>Save</Button>
                </div>
                </div>
        </form>
      )
}
