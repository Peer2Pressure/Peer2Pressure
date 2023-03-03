import { Avatar, Button, TextField } from "@mui/material";
import "./profileSetting.css";
import useFetch from "../../useFetch";
import axios from "axios";
import { useState } from "react";




export default function ProfileSetting() {

    const {data, loading, error} = useFetch("http://localhost:8000/authors/107cb2ca-44ab-488b-bdd2-fcd0edd3c13d/");
    if (data) console.log(data);
    const [userData, setUserData] = useState({
        username: '',
        title: '',
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        avatar: null
    });
    if (loading) return <h1>Loading...</h1>;
    if (error) console.log(error);


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
        formData.append('username', userData.username);
        formData.append('email', userData.email);
        formData.append('password', userData.password);
        formData.append('first_name', userData.first_name);
        formData.append('last_name', userData.last_name);
        if (userData.avatar) {
            formData.append('avatar', userData.avatar, userData.avatar.name);
        }
    
        console.log("usernameeeee: "+userData);
    
        axios
        .post(
            "http://localhost:8000/authors/107cb2ca-44ab-488b-bdd2-fcd0edd3c13d/", 
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
        setUserData({
            ...userData,
            [username] : value
        });
    };

    // console.log("forData: "+formData);
    console.log("username: "+userData.username);
    console.log("email: " + userData.email);    
    console.log('first_namne: '+userData.first_name);
    console.log('last_name: '+userData.last_name);

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
                        <TextField label="First Name" placeholder={data?.first_name} value={userData.first_name} onChange={(e) => handleChange2("first_name", e.target.value)} />
                        <TextField label="Last Name" placeholder={data?.last_name} value={userData.last_name} onChange={(e) => handleChange2("last_name", e.target.value)}/>
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
                    <Button variant="outlined">Cancel</Button>
                    <Button variant="contained" onClick={handleSubmit}>Save</Button>
                </div>
                </div>
        </form>
      )
}
