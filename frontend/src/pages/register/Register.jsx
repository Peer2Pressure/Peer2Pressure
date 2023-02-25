import "./register.css"
import { Link } from "react-router-dom"

const Register = () => {
  return (
    <div className="register">
        <div className="registerCard">
            <div className="registerLeft">
                <h1 className="logo">Peer2Pressure</h1>
            </div>
            <div className="registerRight">
                <div className="registerBox">
                    <input type="Email" placeholder="Email" className="registerInput" />
                    <input type="Password" placeholder="Password (6 or more characters)" className="registerInput" />
                    <button className="registerButton">Join</button>
                    <div className="registerSigninBox">
                        <span className="registerSigninDescription">Already on Peer2Pressure?</span>
                        <Link to="/login">
                            <button className="registerSigninButton">Sign in</button>
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    </div>
  )
}

export default Register