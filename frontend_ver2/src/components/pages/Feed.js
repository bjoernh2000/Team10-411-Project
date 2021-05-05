  
import React, { Component } from 'react'
import './Feed.css'
import TweetBox from './TweetBox'
import { axios, backend_url } from '../../App.js';

export class Feed extends Component {

    constructor(props) {
        super(props)

        this.state = {
            name: ''
        }
    }

    componentDidMount() {
        axios.get(backend_url + "/getProfile")
            .then((response) => {
                this.setState({name: response.data.user.display_name});
            })
            .catch((error) => {
                console.log(error);
            })
    }
    render() {
        return (
            <div className = "feed">
                <div className = "feed__header">
                <h2>
                    Hello {this.state.name}
                </h2>

                <TweetBox />
            

                </div>
            </div>
        )
        
        
    }
}

export default Feed;
