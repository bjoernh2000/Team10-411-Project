import React from 'react'
import './Feed.css'
import TweetBox from './TweetBox'

function Feed() {
    return(
        <div className = "feed">
            <div className = "feed__header">
            <h2>
                Home, Bernie
            </h2>

            <TweetBox />
        

            </div>
        </div>
        
    )
}

export default Feed;
