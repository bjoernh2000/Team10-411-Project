import React, {Component} from 'react';
import './TweetBox.css';
import {Avatar, Button} from "@material-ui/core";
import { axios, backend_url } from '../../App.js';


export class TweetBox extends Component {

    constructor(props) {
        super(props)

        this.state = {
            songID: "",
            image: null
        }
    }

    // componentDidMount() {
    //     axios.get(backend_url + "/getProfile")
    //         .then((response) => {
    //             console.log(response);
    //             this.setState({songID : response.data});
    //         })
    //         .catch((error) => {
    //             console.log(error);
    //         })
    // }


    shareSong = e => {
        e.preventDefault()
        console.log(this.state)
        axios.post(backend_url + "/share_music", {"song_name":this.state.songID}, {headers: {'Content-Type': 'application/json'}}, {withCredentials: true})
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

    }

    render() {
        const { songID } = this.state
        return (
            <div>
                
                {/* {
                    posts.map(post => <div key = {post.data} > {post.title} </div>)
                } */}

                <form onSubmit = {this.shareSong}>
                    <div className = "tweetBox__input">
                    <Avatar src= {this.state.image} />
                        <input placeholder ="What's the music for today?"type = "text" name = "songID" value = {this.state.songID} onChange = {this.onChangeText}/>          
                        {/* <input placeholder ="To who are you sharing to?"type = "text"/> */}
                        <Button className = "tweetBox__tweetButton" onClick={this.shareSong}>
                            Share
                        </Button>
                    </div>
                </form> 
            </div>


            );
    }
    
}

export default TweetBox;


