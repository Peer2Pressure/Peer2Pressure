import { useEffect, useState } from 'react';
import axios from "axios";
import getCsrfToken from "./utils";

// hook <- component but in this case, we don't return jsx (ie. any visual stuff, ui). We only return data and states
// that we may need upon calling the hook.
// installed axios to use this hook
axios.defaults.maxRedirects = 2;

export default function useGetAuthorData() {
    // do an api call whenever we call this hook.

    const [authorID, setAuthorID] = useState(null)
    // const [data, setData] = useState(null);             // set as null because we don't really know the state the data is in initially.
    const [loading, setLoading] = useState(false);      // boolean; set to false initially becuase nothing is loading yet till we call something to load 
    const [error, setError] = useState(null);           // 

    useEffect(() => {
        const getAuthorData = async () => {
            setLoading(true);
            try {
                const csrftoken = getCsrfToken();
                axios.defaults.xsrfHeaderName = 'X-CSRFToken';
                axios.defaults.xsrfCookieName = 'csrftoken';
                setLoading(true);

                const response = await axios.get("/get_author_id/");
                const authorID = response.data.author_id;
                setAuthorID(authorID);
                setLoading(false);
            }   catch(error) {
                setError(error.message);
                
            }   finally {
                setLoading(false);
            }
        };
        getAuthorData();
    }, []);
    return {authorID, loading, error};
}
