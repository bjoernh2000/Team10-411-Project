import React, { Component } from 'react';
import './Profile.css';
import { axios, backend_url } from '../../App.js';
import Cookies from 'js-cookie';
import { Text, Linking } from 'react-native';

export class Profile extends Component {

    constructor(props) {
        super(props)

        this.state = {
            name: '',
            image: null,
            followers: null,
            country: null,
            current_user: null,
            playlists: [],
            playlist_link: []
        }
    }

    componentDidMount() {
        axios.get(backend_url + "/getProfile")
            .then((response) => {
                console.log(response.data);
                this.setState({name: response.data.user.display_name});
                this.setState({image: response.data.user.images[0].url});
                this.setState({followers: response.data.user.followers.total})
                this.setState({country: response.data.user.country})
                this.setState({current_user: response.data.user.id})
                this.setState({playlists: response.data.playlist.playlists.map((p) => p.name)})
                this.setState({playlist_link: response.data.playlist.playlists.map((l) => l.external_urls["spotify"])})
            })
            .catch((error) => {
                console.log(error);
            })
    }

    render() {
        const { name } = this.state

        const playlists_and_links = []
        for (let i = 0; i < this.state.playlists.length; i++) {
            playlists_and_links.push(
                <li className='song-item'>
                    <Text style={{color: 'white', fontSize: 25}}
                        onPress={() => Linking.openURL(this.state.playlist_link[i])}>
                        &nbsp;&nbsp;&nbsp;&nbsp; {this.state.playlists[i]}
                    </Text>
                </li>
            )
        }

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
                            <ol>
                                {playlists_and_links}
                            </ol>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default Profile;