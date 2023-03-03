import { Avatar, Button, TextField } from "@mui/material";
import "./profileSetting.css";
import useFetch from "../../useFetch"
import axios from "axios"
import { useState } from "react"


export default function ProfileSetting() {

    const {data, loading, error} = useFetch("http://localhost:8000/authors/7156bb35-4e95-4911-a6f6-ef9bdc77da75");
    if (data) console.log(data);

    const [userData, setUserData] = useState({
        username: '',
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
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        const formData = new FormData();
        formData.append('username', userData.username);
        formData.append('email', userData.email);
        formData.append('password', userData.password);
        if (userData.avatar) {
            formData.append('avatar', userData.avatar, userData.avatar.name);
        }
    
        axios
        .post(
            "http://localhost:8000/authors/7156bb35-4e95-4911-a6f6-ef9bdc77da75", 
            formData,
            {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            })
        .then((response) => {
            console.log(response.data);
        }).catch((error) => {
            console.log(error);
        });
    };

    const handleChange = (event) => {
        setUserData({
            ...userData,
            [event.target.name]: event.target.value,
        });
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="profileSettingsBox">
                <div className="profileImageBox">
                    <Avatar src={data?.avatar} sx={{width:100, height:100}}/>
                    <input type="file" accept="image/*" onChange={handleFileChange}/>
                    {/* <label htmlFor="avatar-input">
                        <Button component="span">Change image</Button>
                    </label> */}
                </div>
                <div className="profileDetailsBox">
                    <div className="usernameBox">
                        <h2 class="fieldTitle">Username</h2>
                        <TextField label="username" placeholder={data?.username} defaultValue={userData.username} onChange={handleChange}/>
                    </div>
                    <div className="fullNameBox">
                        <h2 className="fieldTitle">Full Name</h2>
                        <TextField label="First Name" placeholder={data?.first_name} defaultValue={userData.first_name} onChange={handleChange} />
                        <TextField label="Last Name" placeholder={data?.last_name} defaultValue={userData.last_name} onChange={handleChange}/>
                        {/* <TextField label="First Name" placeholder={data??.displayName} />
                        <TextField label="Last Name" placeholder={data??.type} /> */}
                    </div>
                    <div className="emailBox">
                        <h2 className="fieldTitle">Email</h2>
                        <TextField label="abc@email.com" placeholder={data?.email} defaultValue={userData.email} onChange={handleChange}/>
                        {/* <TextField label="abc@email.com" placeholder={data??.email}/> */}
    
                    </div>
                    <div className="passwordBox">
                        <h2 className="fieldTitle">Password</h2>
                        <TextField type="password" placeholder="********" defaultValue={userData.password} onChange={handleChange}/>
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
