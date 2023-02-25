import "./share.css";

const Share = () => {

  return (
    <div className="share">
      <div className="shareCard">
        
        <div className="top">
            <div className="shareText">
                <b>Create a Post</b>
            </div>
            <div className="shareImage">
                <input type="file" id="file" style={{display:"none"}} />
                <label htmlFor="file">
                    <div className="uploadImg">
                        <img src = {Image} alt="" />
                        <b>Upload a Photo</b>
                    </div>
                </label>
            </div>
        </div>
        <div className="bottom">
            <textarea name="text" placeholder={"Write something..."} />
        </div>

        <button className="postButton">Post</button>
      </div>
    </div>
  );
};

export default Share;