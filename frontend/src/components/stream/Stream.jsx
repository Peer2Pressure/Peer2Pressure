import Share from "./components/share/share";
import Flipmove from "react-flip-move";

import "./stream.css";
import Post from "../post/Post";
import usePosts from "../../usePosts";

function Stream() {
  const posts = usePosts();

  return (
    <div className="stream">
      <div className="stream__header">
        <h2>Home</h2>
      <Share/>
      </div>
      <div className="stream__posts">
      <Flipmove>
      {posts.map((post) => (
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
      ))}
      </Flipmove>
      </div>
    </div>
  );
}

export default Stream;
