import "./Stream.css";
import Post from "./Post";
import usePosts from "./usePosts";

function Stream() {
  const posts = usePosts();

  return (
    <div className="stream">
      <h1>Hello peeps</h1>
      {posts.map((post) => (
        <Post
          key={post.id}
          displayName={post.displayName}
          username={post.username}
          text={post.text}
          image={post.image}
          avatar={post.avatar}
          likes={post.likes}
          comments={post.comments}
        />
      ))}
    </div>
  );
}

export default Stream;
