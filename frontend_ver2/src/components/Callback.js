import React, {Component} from 'react';
import { SpotifyApiContext } from 'react-spotify-api';
import Cookies from 'js-cookie';
import { axios, backend_url } from '../App.js';
import { getHash } from './getHash'
import { Redirect } from 'react-router'

export class Callback extends Component {

    sendToken(token) {
		
		axios.defaults.withCredentials = true;
        let endpoint = backend_url + "/callback"
            axios.post(endpoint, {token:token}, {headers: {'Content-Type': 'application/json'}}, {withCredentials: true})
            .then((resp) => {
				Cookies.set('flask-session-workaround', resp.headers["x-flask-session-workaround"]);
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
                {/* <p>You are authorized with token: {token}</p> */}
                {this.sendToken(token)}
            </SpotifyApiContext.Provider>
            <Redirect to='/profile'/>
            </div>
        )
    }
}

export default Callback

