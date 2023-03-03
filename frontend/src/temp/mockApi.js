export function getPosts() {
  return Promise.resolve([
    {
      id: 1,
      displayName: "John Doe",
      username: "johndoe",
      text: "Hello world",
      image: "https://picsum.photos/200/300",
      avatar: "https://picsum.photos/50",
      likes: 10,
      comments: 5,
    },
    {
      id: 2,
      displayName: "Jane Smith",
      username: "janesmith",
      text: "Lorem ipsum",
      image: "https://picsum.photos/200/300",
      avatar: "https://picsum.photos/50",
      likes: 20,
      comments: 15,
    },
  ]);
}
