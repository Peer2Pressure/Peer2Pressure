import Share from "../share/Share";
import Flipmove from "react-flip-move";
import { useEffect, useState } from 'react';
import axios from "axios";
import "./stream.css";
import Post from "../post/Post";
import useGetTokens from "../../useGetTokens";

axios.defaults.maxRedirects = 2;

function Stream(props) {
  const { postsUpdated } = props;
  const {tokens, tokenError} = useGetTokens();
  const [inboxPosts, setInboxPosts] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const interval = setInterval(() => {
      async function getPosts() {
        try {
          // let's get the author ID 
          const response1 = await axios.get("/get_author_id/");
          const authorId = response1.data.author_id;
          
          // let's get all the posts under for current author ID
          const response2 = await axios.get("/authors/" + authorId + "/inbox", {
            headers:{
                "Authorization": tokens[window.location.hostname]
            }
          });
          setInboxPosts(response2.data.items);

        } catch(error) {
          setError(error);
        };
      };
  
      getPosts();
    }, 1500);
    return () => clearInterval(interval);
  }, [postsUpdated, tokens]);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!inboxPosts) {
    return <div>Loading...</div>;
  }

  const sortedInboxPosts = inboxPosts.sort((a, b) => {
    return new Date(b.published) - new Date(a.published);
  });

  return (
    <div className="stream">
        <Flipmove className="flippy">
          {sortedInboxPosts.map((post) => (
            <div className="stream__posts" key={post.id}>
              <Post
                className="post"
                key={post.id}
                id={post.id}
                host={new URL(post.origin).hostname}
                displayName={post.author.displayName}
                username={post.author.displayName}
                text={post.content}
                image_url={post.image_url}
                avatar={post.author.profileImage}
                likes={post.likes}
                comments={post.comments}
                contentType={post.contentType}
                title={post.title}
              />
            </div>
          ))}
        </Flipmove>
    </div>

  );
}

export default Stream;
