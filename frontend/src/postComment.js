import axios from "axios";

function postComment(authorId,postId, commentText) {
  const post = async () => {
    try {
      const response = await axios.post(`/authors/${authorId}/posts/${postId}/comments/`, {
        comment: commentText,
      });
      console.log(response.data); // optional, log the response data
    } catch (error) {
      console.error(error);
    }
  };

  return post;
}

export default postComment;
