import "./login.css"
import { Link } from "react-router-dom"

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
                    <button className="signinButton">Sign in</button>
                    <div className="joinBox">
                        <span className="joinDescription">New to Peer2Pressure?</span>
                        <Link to="/register">
                            <button className="joinButton">Join Now</button>
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    </div>
  )
}

export default Login