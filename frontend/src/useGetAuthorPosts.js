import { useState, useEffect } from "react";
import axios from "axios";

function usePostAuthorPosts() {
  const [authorID, setAuthorID] = useState(null);
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getPosts = async() => {
      try {
        // let's get the author ID 
        const response = await axios.get("/get_author_id/");
        setAuthorID(response.data);
        console.log("author ID: " + authorID);

        // let's get all the posts under this author ID
        const response2 = await axios.get("/authors/" + authorID + "/posts/");
        console.log("/authors/" + authorID + "/posts/");
        setPosts(response2.data);

      } catch(error) {
        setError(error);
      };
    };
    getPosts();
  },[]);
  return {posts, error};
}

export default usePostAuthorPosts;
