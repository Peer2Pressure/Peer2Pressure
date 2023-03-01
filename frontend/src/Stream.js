
import './Stream.css'
import Post from './Post'
import React, { useState, useEffect } from "react";
function usePosts() {
    const [posts, setPosts] = useState([]);
  
    useEffect(() => {
      // Fetch data from backend API
      fetch("/posts")
        .then((response) => response.json())
        .then((data) => setPosts(data));
    }, []);
  
    return posts;
  }
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

export default Stream