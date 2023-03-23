import Share from "../share/Share";
import Flipmove from "react-flip-move";
import { useEffect, useState } from 'react';

import "./stream.css";
import Post from "../post/Post";

// import usePosts from "../../usePosts";
import usePostAuthorPosts from "../../useGetAuthorPosts";


function Stream() {
  // const posts = samplePosts;
  // // const posts = usePosts();
  // const [posts, setPosts] = useState(null);

  const {posts, error} = usePostAuthorPosts();
  console.log("items 11@:  ", posts)


  // setPosts(inbox["items"])
  console.log("$$123123 posts", posts.items)

  const inbox_posts = posts.items
  console.log("inbox poss", inbox_posts)

  return (
    <div className="stream">
      <div className="stream__header">
        {/* <h2>Home</h2> */}
        {/* <Share/> */}
      </div>
      <div  >
      <Flipmove>
      {inbox_posts.map((post) => (
        <div className="stream__posts" key={post.id}>
          <Post
            key={post.id}
            displayName={post.displayName}
            username={post.username}
            text={post.caption}
            image={"http://localhost:8000"+post.image}
            avatar={post.avatar}
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
