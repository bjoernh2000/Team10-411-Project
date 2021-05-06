import React from 'react'
import { SpotifyAuth, Scopes } from 'react-spotify-auth'
import { frontend_url, spotify_client_id } from '../../App.js';
import 'react-spotify-auth/dist/index.css'

function SignIn() {
    return (
        <div className='sign-in'>
            <SpotifyAuth
                            redirectUri= {`${frontend_url}/callback`}
                            clientID={spotify_client_id}
                            scopes={[Scopes.userReadPrivate, Scopes.userReadEmail, Scopes.playlistReadPrivate, Scopes.userLibraryRead]}
                        />
        </div>
    )
}

export default SignIn
