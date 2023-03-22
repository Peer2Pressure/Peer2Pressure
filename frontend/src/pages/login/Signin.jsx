import React from 'react'
import "./signin.css"

export default function Signin() {
  return (
    <div class="signin">
        <div class="signinCard">
            <div class="signinLeft">
                <h1 class="logo">Peer2Pressure</h1>
            </div>
            <div class="signinRight">
                <div class="signinBox">
                    <div class="formHead">
                        {/* <h1>p2p</h1> */}
                    </div>
                    <div class="formBox">
                        <form action="{% url 'signin' %}" method="post">
                            {/* {% csrf_token %} */}
                            <input type="text" name="username" placeholder="Username" class="signinInput" />
                            <input type="password" name="password" placeholder="Password" class="signinInput" />
                            <div class="buttonBox">
                                <input type="submit" class="signinButton" value="Sign In"/>
                            </div>
                        </form>
                    </div>
                    <div class="joinBox">
                        <span class="joinDescription">New to Peer2Pressure?</span>
                        <div class="join-button-container">
                            <a href="/signup" class="join-button-text">Join Now</a>
                        </div>
                    </div>                    
                </div>
            </div>
        </div>
    </div>
  )
}
