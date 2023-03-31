import { useState, useEffect } from "react";
import axios from "axios";

axios.defaults.maxRedirects = 2;

function useGetNodeAPIEndpoints() {
    const [endpoints, setEndpoints] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getEndpoints = async() => {
            try {
                const response = await axios.get(`/nodes/api_endpoints/`);
                setEndpoints(response.data.items)
            } catch (error) {
                setError(error);
            }
        }; 
        getEndpoints();
    }, []);
    return endpoints;
}

export default useGetNodeAPIEndpoints;

