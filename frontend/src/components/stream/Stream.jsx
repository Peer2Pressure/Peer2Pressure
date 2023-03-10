import Share from "../share/Share";
import Flipmove from "react-flip-move";

import "./stream.css";
import Post from "../post/Post";
import usePosts from "../../usePosts";

function Stream() {
  const posts = usePosts();

  return (
    <div className="stream">
      <div className="stream__header">
        {/* <h2>Home</h2> */}
        {/* <Share/> */}
      </div>
      <div  >
      <Flipmove>
      {posts.map((post) => (
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
