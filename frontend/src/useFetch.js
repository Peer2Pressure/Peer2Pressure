import { useEffect, useState } from 'react';
import axios from "axios";

// hook <- component but in this case, we don't return jsx (ie. any visual stuff, ui). We only return data and states
// that we may need upon calling the hook.
// installed axios to use this hook

axios.defaults.maxRedirects = 2;

export default function useFetch(url) {
    // do an api call whenever we call this hook.

    const [data, setData] = useState(null);             // set as null because we don't really know the state the data is in initially.
    const [loading, setLoading] = useState(false);      // boolean; set to false initially becuase nothing is loading yet till we call something to load 
    const [error, setError] = useState(null);           // 

  useEffect(() => {                                     // insert url to get in touch with the api
    setLoading(true);                                   // set loading to true after a call to an api is made 
    axios
    .get(url)
    .then((response) => {
        setData(response.data);
    }).catch((error) => {                               // catch will be call if there's an error 
        setError(error);
    }).finally(() => {
        setLoading(false);                              // Loading phase is done when reached 
    });
  }, [url]);                                            // useEffect need dependency array which will have url 

  // console.log(data);
  return {data, loading, error};                        // return an object containing the three      
}
