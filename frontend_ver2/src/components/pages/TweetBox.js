import React from 'react';
import './TweetBox.css';
import {Avatar, Button} from "@material-ui/core";

function TweetBox() {
    return (
        <div className = "tweetBox">
            <form>
                <div className = "tweetBox__input">
                <Avatar src="https://media-exp1.licdn.com/dms/image/C5603AQHofXSvVY29HA/profile-displayphoto-shrink_400_400/0/1602271449845?e=1625097600&v=beta&t=7cI55IiFmLLzcUL2IsG1nnjbyNHHZFmuaG5KbgIZoCw" />
                    <input placeholder ="What's the music for today?"type = "text"/>
                    <br/>                    
                    <input placeholder ="To who are you sharing to?"type = "text"/>
                    <Button className = "tweetBox__tweetButton">
                        Share
                    </Button>
                </div>
            </form>
        </div>
        );
    
}

export default TweetBox;