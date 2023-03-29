import { useState, useEffect } from "react";
import axios from "axios";

function useGetNodeHosts() {
    const [hosts, setHosts] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getHosts = async() => {
            try {
                const response = await axios.get(`/nodes/hostnames/`);
                setHosts(response.data.items)
            } catch (error) {
                setError(error);
            }
        }; 
        getHosts();
    }, []);
    return hosts;
}

export default useGetNodeHosts;

