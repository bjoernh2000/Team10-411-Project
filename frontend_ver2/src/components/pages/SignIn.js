import React from 'react'
import { SpotifyAuth, Scopes } from 'react-spotify-auth'
import 'react-spotify-auth/dist/index.css'

function SignIn() {
    return (
        <div className='sign-in'>
            <SpotifyAuth
                            redirectUri='http://localhost:3000/callback'
                            clientID=''
                            scopes={[Scopes.userReadPrivate, Scopes.userReadEmail]}
                        />
        </div>
    )
}

export default SignIn
