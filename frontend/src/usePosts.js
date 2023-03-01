import { useState, useEffect } from "react";
import axios from "axios";

function usePosts() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios
      .get("/posts")
      .then((response) => setPosts(response.data))
      .catch((error) => console.error(error));
  }, []);

  return posts;
}

export default usePosts;
