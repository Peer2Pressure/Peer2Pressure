import { useState, useEffect } from "react";
import axios from "axios";

function usePosts() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/posts/")
      .then((response) => setPosts(response.data))
      .catch((error) => console.error(error));
      
  }, []);
  console.log(posts);

  return posts;
}

export default usePosts;
