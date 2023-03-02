import { useState, useEffect } from "react";
import axios from "axios";

function usePosts() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/authors/0898446d-c1ff-4845-8aba-510997a2c223/posts")
      .then((response) => setPosts(response.data))
      .catch((error) => console.error(error));
      
  }, []);
  console.log(posts);

  return posts;
}

export default usePosts;
