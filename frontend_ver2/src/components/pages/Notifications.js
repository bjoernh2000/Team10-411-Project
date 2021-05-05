import React, { Component } from 'react';
import { axios, backend_url } from '../../App.js';
import './Notifications.css';




export class Notifications extends Component {

    constructor(props) {
        super(props)

        this.state = {
            notificationNum: null,
            user: "",
            friend: "",
            type: null
        }
    }

    componentDidMount() {
        axios.get(backend_url + "/notifications")
            .then((response) => {
                console.log(response);
                console.log(response.data.length);
                // console.log(response.headers.content-length);
            })
            .catch((error) => {
                console.log(error);
            })
    }

    render() {

        return (
            <div>
               hello
            </div>
        );
    }
}

export default Notifications;


// export default function Notifications() {
//     return (
//         <>
//         <header>
//             <h1>BAD DJ ­-  Notifications</h1>
//         </header>
//         <div class="main">
//             <table>
//                 <div class="notif-odd-row">
//                     <tr>
//                         <td class="notif-info">Adam has sent you a friend
//                                 request.</td>
//                         <td><a href="#"><div class="button-link">Accept</div></a></td>
//                         <td><a href="#"><div class="button-link">Reject</div></a></td>
//                     </tr>
//                 </div>
//                 <div class="notif-even-row">
//                     <tr>
//                         <td class="notif-info">Della has commented on your playlist.</td>
//                         <td><a href="#"><div class="button-link">View</div></a></td>
//                         <td><a href="#"><div class="button-link">Ignore</div></a></td>
//                     </tr>
//                 </div>
//             </table>
//         </div>
//         </>
//     );
// }