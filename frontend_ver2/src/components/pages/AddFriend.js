import React, { Component } from 'react'
import './TweetBox.css';
import {Avatar, Button} from "@material-ui/core";
import {axios, backend_url } from '../../App.js';

export class AddFriend extends Component {
    constructor(props) {
        super(props);
        this.state = {
            friendName:"",
            image: null
        };
    }

    // @app.route("/friends/add")
    // @cross_origin(origin=FRONTEND_DOMAIN, headers=SESSION_LOGIN_HEADERS)
    // @login_required
    // def add_friend(current_user):
    //     user_id = current_user.user_id
    //     friend_user_id = request.args["friend_user_id"]
    //     mongo.db.friends.insert({"user_id": user_id, "friend_user_id": friend_user_id})
    //     return ('', 204)

    sendFriendRequest = e => {
        e.preventDefault()
        console.log(this.state)
        const url = backend_url + "/friends/add";
        // var current_user = {
        //     "user_id": user_id
        // }
        axios.post(url, this.state.friendName)
        .then(response => {
            console.log(response)
        })
        .catch(error => {
            console.log(error)
        })
    }

    onChangeText = e => {
        this.setState({[e.target.name]: e.target.value})
    }

    componentDidMount() {
        axios.get(backend_url + "/getProfile")
            .then((response) => {
                console.log(response.data);
                this.setState({image: response.data.images[0].url});
            })
            .catch((error) => {
                console.log(error);
            })
    }

    render() {
        const { friendName } = this.state
        return (
            <div>
                <form onSubmit = {this.sendFriendRequest}>
                <div className = "tweetBox__input">
                <Avatar src= {this.state.image} />
                    <input placeholder ="Friend to add?" type ="text" name = "friendName" value = {this.state.friendName} onChange = {this.onChangeText}/>
                    <Button className = "tweetBox__tweetButton" onClick={this.sendFriendRequest}>
                        Add
                    </Button>
                </div>
            </form>
            </div>
        )
    }
}

export default AddFriend
