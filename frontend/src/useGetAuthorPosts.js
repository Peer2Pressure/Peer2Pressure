import { useState, useEffect } from "react";
import axios from "axios";

function usePostAuthorPosts() {
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getPosts = async() => {
      try {
        // let's get the author ID 
        const response1 = await axios.get("/get_author_id/");
        const authorId = response1.data.author_id;

        console.log("author ID: " + authorId);
        // authorId = "1ead7fea-2483-463d-94d7-6e0ea244a1ff"
        // let's get all the posts under this author ID
        const response2 = await axios.get("/authors/" + authorId + "/inbox/");
        console.log("/authors/" + authorId + "/inbox/");
        setPosts(response2.data);

      } catch(error) {
        setError(error);
      };
    };
    console.log("author ID: " + authorID);
    console.log("hEYLO :","/authors/" + authorID + "/posts/");
    getPosts();
  },[]);
  return {posts, error};
}

export default usePostAuthorPosts;
