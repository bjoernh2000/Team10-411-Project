import React, { Component } from 'react'
import './TweetBox.css';
import {Avatar, Button} from "@material-ui/core";

export class ShareMusic extends Component {
    constructor(props) {
        super(props);
        this.state = {name:""};
    }

    sendFriendRequest() {

        // send friend request with a axios.post
    }

    onChangeText(event) {
        this.setState({name : event.target.value});
    }

    render() {
        return (
            <div>
                <form>
                <div className = "tweetBox__input">
                <Avatar src="https://media-exp1.licdn.com/dms/image/C5603AQHofXSvVY29HA/profile-displayphoto-shrink_400_400/0/1602271449845?e=1625097600&v=beta&t=7cI55IiFmLLzcUL2IsG1nnjbyNHHZFmuaG5KbgIZoCw" />
                    <input placeholder ="Friend to add?"type = "text" value={this.state.name} onChange={(e) => {this.onChangeText(e)}}/>                 
                    <Button className = "tweetBox__tweetButton" onClick={this.sendFriendRequest}>
                        Add
                    </Button>
                </div>
            </form>
            </div>
        )
    }
}

export default ShareMusic
