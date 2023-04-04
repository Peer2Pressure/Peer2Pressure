
import Flipmove from "react-flip-move";
import { useEffect, useState } from 'react';
import axios from "axios";
import "./stream.css";
import Post from "../post/Post";
import useGetTokens from "../../useGetTokens";

function Stream(props) {
  const { authorData, authorID, tokens, filterParam } = props;
  // const { filterParam } = props;
  // const {tokens, tokenError} = useGetTokens();
  const [inboxPosts, setInboxPosts] = useState([]);
  const [error, setError] = useState(null);
  console.log("filterParam: ", filterParam);

  useEffect(() => {  
    const sse = new EventSource('http://localhost:8000/authors/69313508-2320-4b04-b44f-668090e85394/inbox/stream/',
    { 
      // withCredentials: true,
      // headers: {
      //   // "Authorization": "Basic " + btoa("p2padmin:p2padmin"),
      //   // "Origin": "http://localhost:8000"
      // }
    });  
    
    function updateInboxPosts(newPost) {
      setInboxPosts(prevInboxPosts => {
        const existingPostIndex = prevInboxPosts.findIndex(post => post.id === newPost.id);

        if (existingPostIndex > -1) {
          // Update the existing post
          const updatedPosts = [...prevInboxPosts];
          updatedPosts[existingPostIndex] = newPost;
          return updatedPosts;
        } else {
          // Add the new post to the state
          return [newPost, ...prevInboxPosts];
        }
      });
    }

    
    sse.onopen = () => {
      console.log("Event source connection open.")
    };

    sse.onmessage = (e) => {
      console.log("E ====== ", e)
      const newPost = JSON.parse(e.data);
      if (Object.keys(newPost).length !== 0) {
        updateInboxPosts(newPost);
      } else {
        console.log("Server is testing connection")
      }
      

    };

    sse.onerror = (e) => {
      if (e.target.readyState === EventSource.CLOSED) {
        console.log('EventSource connection has been closed.');
        sse.close();
      } else if (e.target.readyState === EventSource.CONNECTING) {
        console.log('EventSource connection is being re-established.');
      } else {
        console.log('An unknown error occurred:', e);
      }
      
    };

    // Add a beforeunload event listener to close the EventSource
    const handleBeforeUnload = () => {
      sse.close();
    };
    window.addEventListener('beforeunload', handleBeforeUnload);

    // Clean up the beforeunload event listener when the component is unmounted
    return () => {
      sse.close();
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };

  }, []);


  // useEffect(() => {
  //   axios.defaults.maxRedirects = 5;
  //   const interval = setInterval(() => {
  //     async function getPosts() {
  //       try {
  //         // // let's get the author ID 
  //         // const response1 = await axios.get("/get_author_id/");
  //         // const authorId = response1.data.author_id;
          
  //         // let's get all the posts under for current author ID
  //         const response2 = await axios.get("/authors/" + authorID + "/inbox/", {
  //           headers:{
  //               "Authorization": tokens[window.location.hostname]
  //           }
  //         });
  //         if (!filterParam) {
  //         // Filter the posts based on the visibility variable
  //         const privatePosts = response2.data.items.filter(post => post.visibility === 'PRIVATE');
  //         setInboxPosts(privatePosts);
  //         }
  //         else {
  //           const publicPosts = response2.data.items.filter(post => post.visibility === 'PUBLIC' || post.visibility === 'FRIENDS');
  //           setInboxPosts(publicPosts);
  //         }
  //       } catch(error) {
  //         setError(error);
  //       };
  //     };
  
  //     getPosts();
  //   }, 1500);

  //   return () => clearInterval(interval);
  // }, [tokens]);



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
                // postAuthorID={post.author.id}
                id={post.id}
                host={new URL(post.author.host).hostname}
                displayName={post.author.displayName}
                username={post.author.displayName}
                text={post.content}
                avatar={post.author.profileImage}
                comments={post.comments}
                contentType={post.contentType}
                title={post.title}
                origin={post.origin}
                visibility={post.visibility}
                source={post.source}
                postAuthorID2={post.author.id}
                authorData={authorData}
                authorID={authorID}
                tokens={tokens}
                // likes={post.like}
              />
            </div>
          ))}
        </Flipmove>
    </div>

  );
}

export default Stream;