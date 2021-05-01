import React, {Component} from 'react';
import { SpotifyApiContext } from 'react-spotify-api';
import Cookies from 'js-cookie';
import axios from 'axios';
import { getHash } from './getHash'

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
        const accessToken = getHash().access_token
        console.log(accessToken);
        if (accessToken) {
            document.cookie = `spotifyAuthToken=${accessToken}; max-age=${60 * 60};`
        }
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

