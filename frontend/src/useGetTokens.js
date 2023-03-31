import { useState, useEffect } from "react";
import axios from "axios";

axios.defaults.maxRedirects = 2;

function useGetTokens() {
    const [tokens, setTokens] = useState("");
    const [error, setError] = useState(null);

    useEffect(() => {
        const getTokens = async() => {
            try {
                const response = await axios.get(`/nodes/tokens/`);
                // console.log("RESPONSE DATA", response.data);
                setTokens(response.data)
            } catch (error) {
                setError(error);
            }
        }; 
        getTokens();
    }, []);
    return {tokens, error};
}

export default useGetTokens;

