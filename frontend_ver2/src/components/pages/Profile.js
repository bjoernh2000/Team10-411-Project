import React, { Component } from 'react';
import './Profile.css';
import { axios, backend_url } from '../../App.js';
import Cookies from 'js-cookie';

export class Profile extends Component {

    constructor(props) {
        super(props)

        this.state = {
            name: '',
            image: null,
            followers: null,
            country: null,
            current_user: null
        }
    }

    componentDidMount() {
        axios.get(backend_url + "/getProfile")
            .then((response) => {
                console.log(response.data);
                this.setState({name: response.data.display_name});
                this.setState({image: response.data.images[0].url});
                this.setState({followers: response.data.followers.total})
                this.setState({country: response.data.country})
                this.setState({current_user: response.data.id})
            })
            .catch((error) => {
                console.log(error);
            })
    }

    render() {
        const { name } = this.state
        return (
            <div>
                <div className='profile-container'>
                    <div className='profile-header'>
                        <div>
                            <img style={{width:"200px",height:"200px",borderRadius:"100px"}} 
                            src= {this.state.image} alt=""/>
                        </div>
                        <div className='text'>
                            <div className='name'>
                                <h4>
                                   {this.state.name}
                                </h4>
                            </div>
                            <div className='friends'>
                                <h5>
                                    Country:  {this.state.country} &nbsp;&nbsp;|&nbsp;&nbsp; {this.state.followers} Followers
                                </h5>
                            </div>
                        </div>
                    </div>
                </div>
                <div className='bottom-container'>
                    <div className='main-playlist'>
                        <h4>
                            {this.state.name}'s Playlist
                        </h4>
                        <div className='songs'>
                            <ul>
                                <li className='song-item'>
                                1&nbsp;&nbsp;&nbsp;&nbsp;Song Name #1
                                </li>
                                <li className='song-item'>
                                2&nbsp;&nbsp;&nbsp;&nbsp;Song Name #2
                                </li>
                                <li className='song-item'>
                                3&nbsp;&nbsp;&nbsp;&nbsp;Song Name #3
                                </li>
                                <li className='song-item'>
                                4&nbsp;&nbsp;&nbsp;&nbsp;Song Name #4
                                </li>
                                <li className='song-item'>
                                5&nbsp;&nbsp;&nbsp;&nbsp;Song Name #5
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Profile;