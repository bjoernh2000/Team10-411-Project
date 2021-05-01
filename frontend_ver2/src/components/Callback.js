import React, {Component} from 'react';
import { SpotifyApiContext } from 'react-spotify-api';
import Cookies from 'js-cookie';
import axios from 'axios';

export class Callback extends Component {

    sendToken(token) {
        let endpoint = "http://127.0.0.1:8080/callback"
            axios.post(endpoint, {token:token}, {headers: {'Content-Type': 'application/json'}})
            .then((resp) => {
                console.log(resp);
            })
            .catch((err) => {
                console.log(err);
            })
    }

    render() {
        const token = Cookies.get("spotifyAuthToken");
        return (
            <div>
                <SpotifyApiContext.Provider value={token}>
                <p>You are authorized with token: {token}</p>
                {this.sendToken(token)}
            </SpotifyApiContext.Provider>
            </div>
        )
    }
}

export default Callback

