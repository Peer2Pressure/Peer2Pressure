import "./login.css"


const Login = () => {
  return (
    <div className="signin">
        <div className="signinCard">
            <div className="signinLeft">
                <h1 className="logo">Peer2Pressure</h1>
            </div>
            <div className="signinRight">
                <div className="signinBox">
                    <input type="Email" placeholder="Email" className="signinInput" />
                    <input type="Password" placeholder="Password" className="signinInput" />
                    <button variant="contained" className="signinButton">Sign in</button>
                    <div className="joinBox">
                        <span className="joinDescription">New to Peer2Pressure?</span>
                        <button className="joinButton">Join Now</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
  )
}

export default Login