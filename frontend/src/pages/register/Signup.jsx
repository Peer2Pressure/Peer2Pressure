import React from 'react'
import "./signup.css"

export default function Signup() {
  return (
    <div class="register">
        <div class="registerCard">
            <div class="registerLeft">
                <h1 class="logo">Peer2Pressure</h1>
            </div>
            <div class="registerRight">
                <div class="registerBox">
                    <form action="{% url 'signup' %}" method="post">
                    {/* {% csrf_token %} */}
                        <div className="registerInputs">
                            <input type="text" name="name" placeholder="Name" class="registerInput" />
                            <input type="text" name="username" placeholder="Username" class="registerInput" />
                            <input type="email" name="email" placeholder="Email" class="registerInput" />
                            <input type="password" name="password" placeholder="Password" class="registerInput" />
                            <input type="password" name="password2" placeholder="Re-Enter Password" class="registerInput" />
                            <input type="submit" class="registerButton" value="Join"/>
                            <div class="registerSigninBox">
                                <span class="registerSigninDescription">Already on Peer2Pressure?</span>
                                {/* <!-- <link to="/signin">
                                    <button class="registerSigninButton">Sign in</button>
                                </link> --> */}
                                <div class="register-button-container">
                                    <a href="/signin" class="register-button-text">Sign In</a>
                                </div>
                            </div> 
                        </div>
                        
                    </form>   
                </div>
            </div>
        </div>
    </div>
  )
}
