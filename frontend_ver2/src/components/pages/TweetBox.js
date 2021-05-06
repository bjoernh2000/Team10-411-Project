import React, {Component} from 'react';
import './TweetBox.css';
import {Avatar, Button} from "@material-ui/core";
import { axios, backend_url } from '../../App.js';
import { Text, Linking } from 'react-native';

export class TweetBox extends Component {

    constructor(props) {
        super(props)

        this.state = {
            songID: "",
            image: null,
            song_names: []
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
        axios.get(backend_url + "/getProfile")
            .then((response) => {
                console.log(response.data.user.images[0].url);
                this.setState({image: response.data.user.images[0].url})
                this.setState({songs: response.data.song});
            })
            .catch((error) => {
                console.log(error);
            })

        axios.get(backend_url + "/music_feed")
            .then((response) => {
                console.log(response);
                this.setState({song_names: response.data.map((s) => s.song.name)});
                console.log(this.state.song_names)
            })
            .catch((error) => {
                console.log(error);
            })
    }

    render() {
        const { songID } = this.state.songID

        const display_s_names = []
        for (let i = 0; i < this.state.song_names.length; i++) {
            display_s_names.push(
                <div className = 'song-item'>
                    <Text style={{color: 'white', fontSize: 25}}>
                        &nbsp;&nbsp;&nbsp;&nbsp; {this.state.song_names[i]}
                    </Text>
                </div>
            )
        }

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

                    <div className = "display__feed">
                        <ol>
                            {display_s_names}
                        </ol>
                    </div>
                </form> 
            </div>


            );
    }
    
}

export default TweetBox;


