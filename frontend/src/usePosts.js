import { useState, useEffect } from "react";
import axios from "axios";

function usePosts() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/authors/b1411a6f-2314-4195-9b23-8055f2b42b79/posts")
      .then((response) => setPosts(response.data))
      .catch((error) => console.error(error));
      
  }, []);
  console.log(posts);

  return posts;
}

export default usePosts;
