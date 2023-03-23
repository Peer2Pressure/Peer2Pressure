import Share from "../share/Share";
import Flipmove from "react-flip-move";
import { useEffect, useState } from 'react';
import axios from "axios";
import "./stream.css";
import Post from "../post/Post";

function Stream() {
  const [posts, setPosts] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function getPosts() {
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
 
    getPosts();
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!posts) {
    return <div>Loading...</div>;
  }

  const inbox_posts = posts.items;
  console.log("inbox poss", inbox_posts);

  return (
    <div className="stream">
      <div className="stream__header">
        {/* <h2>Home</h2> */}
        {/* <Share/> */}
      </div>
      <div>
        <Flipmove>
          {inbox_posts.map((post) => (
            <div className="stream__posts" key={post.id}>
              <Post
                key={post.id}
                displayName={post.author.displayName}
                username={post.author.displayName}
                text={post.content}
                image={post.image}
                avatar={post.author.profileImage}
                likes={post.likes}
                comments={post.comments}
              />
            </div>
          ))}
        </Flipmove>
      </div>
    </div>
  );
}

export default Stream;
