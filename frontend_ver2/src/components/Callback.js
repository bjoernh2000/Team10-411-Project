import React, {Component} from 'react';
import { SpotifyApiContext } from 'react-spotify-api';
import Cookies from 'js-cookie';
import axios from 'axios';
import { getHash } from './getHash'

export class Callback extends Component {

    sendToken(token) {
		
		axios.defaults.withCredentials = true;
        let endpoint = "http://127.0.0.1:8080/callback"
            axios.post(endpoint, {token:token}, {headers: {'Content-Type': 'application/json'}}, {withCredentials: true})
            .then((resp) => {
				
				// This code only needs to be present on pages that handle logging in... so probably only this one.
				// The axios.defaults.headers settings make sure the auth header is included in all axios requests.
				Cookies.set('flask-session-workaround', resp.headers["x-flask-session-workaround-because-cross-site-cookies-are-death"]);
				axios.defaults.headers.get['X-Flask-Session-Workaround-Because-Cross-Site-Cookies-Are-Death'] = Cookies.get('flask-session-workaround')
				axios.defaults.headers.post['X-Flask-Session-Workaround-Because-Cross-Site-Cookies-Are-Death'] = Cookies.get('flask-session-workaround')
				
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

