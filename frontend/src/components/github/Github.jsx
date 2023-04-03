import "./github.css"

import React from 'react'
import { useEffect, useState} from "react";
import axios from "axios";

const GitHub = ({username}) => {

    // const [events, setEvents] = useState([]);

    // useEffect(() => {
    //     const fetchData = async () => {
    //         try {
    //             const response = await axios.get(`https://api.github.com/users/jteengfo/events`);
    //             setEvents(response.data);
    //         } catch(error) {
    //             console.log('Error in retrieving github activity', error);
    //         }
    //     };
    //     fetchData();
    // }, [username]);

    return(
        <div id="feed">
            GitHubAc
        </div>
    );

};

export default GitHub
