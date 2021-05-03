import React from 'react'
import { SpotifyAuth, Scopes } from 'react-spotify-auth'
import { frontend_url } from '../../App.js';
import 'react-spotify-auth/dist/index.css'

function SignIn() {
    return (
        <div className='sign-in'>
            <SpotifyAuth
                            redirectUri= {`${frontend_url}/callback`}
                            clientID='578597110fa642daaef83cd9c122d1d9'
                            scopes={[Scopes.userReadPrivate, Scopes.userReadEmail]}
                        />
        </div>
    )
}

export default SignIn
