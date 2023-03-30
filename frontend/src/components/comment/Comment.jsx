import React, { forwardRef } from 'react'
import { Avatar } from '@mui/material'
import './comment.css'

import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';

// const Comment = forwardRef(({profileImage, displayName, comment }, ref) => {

export default function Comment() {





    return (
        <div className="commentContainer">
            <div className="commentHeader">
                <div className="avatarContainer">
                    {/* <Avatar sx={{width: 24, height: 24}} src={profileImage}/> */}
                    <Avatar sx={{width: 24, height: 24}}/>
                </div>
                <div className="authorAndCommentContainer">
                    <div className="authorContainer">
                        <h5>John Doe</h5>
                        {/* <h3>{displayName}</h3> */}
                    </div>
                    <div className="commentBody">
                        <p>To be or not to be, that is the question.</p>
                        {/* <p>{comment}</p> */}
                    </div>
                </div>
            </div>
            <div className="iconContainer">
                {/* {like? (<><FavoriteIcon fontSize="small" /></>)
                :(<><FavoriteBorderIcon fontSize="small" /></>)} */}
                <FavoriteIcon fontSize='small'/>

            </div>
        </div>
    )
};
