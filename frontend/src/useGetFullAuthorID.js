import React from 'react'
import axios from 'axios';
import { useState, useEffect } from 'react';
import useGetAuthorData from './useGetAuthorData';

export default function useGetFullAuthorID() {
    // do an api call whenever we call this hook.

    // const [authorUUID, setAuthorUUID] = useState(null);
    const [authorIDD, setAuthorID] = useState(null);
    useEffect(() => {
        const getAuthorID = async () => {
            try {

                const response = await axios.get("/get_author_id/");
                const uuid = response.data.author_id;
            
                const response2 = await axios.get("/authors/" + uuid + '/');
                const authorID = response2.data.id;
                setAuthorID(authorID);

            }   catch(error) {
                console.log(error);
            }   
        };
        getAuthorID();
    }, []);
    console.log("UAOAHSDJ: ", authorIDD)
    return {authorIDD};
}
