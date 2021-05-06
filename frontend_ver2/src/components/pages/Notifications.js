import React, { Component } from 'react';
import { axios, backend_url } from '../../App.js';
import './Notifications.css';
import { Text, Linking } from 'react-native';



export class Notifications extends Component {

    constructor(props) {
        super(props)

        this.state = {
            notifications: [],
            type: [],
            notification_id: []
        }
    }

    // viewNotification() {
    //     axios.post(backend_url + '/notification_button_pressed',
    //     (
    //         notification_id: {this.state.notification_id[0]}
    //         button: 
    //     )
    //       .then((response) => {
    //         console.log(response);
    //       }).catch((error) => {
    //         console.log(error);
    //       });
    // }

    // shareSong = e => {
    //     e.preventDefault()
    //     console.log(this.state)
    //     axios.post(backend_url + "/share_music", {"song_name":this.state.songID}, {headers: {'Content-Type': 'application/json'}}, {withCredentials: true})
    //     .then(response => {
    //         console.log(response)
    //     })
    //     .catch(error => {
    //         console.log(error)
    //     })
    // }


    onAccept(notification_id) {
		axios.post("/notification_button_pressed", {"button": "Accept", "notification_id": notification_id})
	}
	onReject(notification_id) {
		axios.post("/notification_button_pressed", {"button": "Reject", "notification_id": notification_id})
	}
	onDismiss(notification_id) {
		axios.post("/notification_button_pressed", {"button": "Dismiss", "notification_id": notification_id})
	}

    componentDidMount() {
        axios.get(backend_url + "/notifications")
            .then((response) => { 
                console.log(response)               
                this.setState({notifications: response.data.map((p) => p.text)})
                this.setState({type: response.data.map((p) => p.type)})
                this.setState({notification_id: response.data.map((p) => p.notification_id)})
            })
            .catch((error) => {
                console.log(error);
            })
    }


    render() {
        const { notifications } = this.state
        const notification_list = []
        for (let i = 0; i < this.state.notifications.length; i++) {
            
                notification_list.push(
                    <li className={i%2==0?'even-notif':'notif-item'}>
                    <h2>
                        {this.state.notifications[i]}
                    </h2>
                </li> )

                if (this.state.type[i] == "NOTIFICATION") {
                    notification_list.push(
                        <a href="#"><div class="button-link" onClick={this.onAccept(this.state.notification_id[i])}>View</div></a>
                    )
                    notification_list.push(
                        <a href="#"><div class="button-link" onClick={this.onReject(this.state.notification_id[i])}>Ignore</div></a>
                    )
                } else if (this.state.type[i]  == "FRIEND_REQUEST") {
                    notification_list.push(
                        <a href="#"><div class="button-link" >Accept</div></a>
                    )
                    notification_list.push(
                        <a href="#"><div class="button-link"onClick={this.onDismiss(this.state.notification_id[i])}>Reject</div></a>
                    )
                }
                   
        } 




        return (
            <div>
            <header>
               <h1>BAD DJ ­-  Notifications</h1>
            </header>
            <div class="notif-row">
                <table>
            <ul>
            {notification_list} 
            {/* {notification_type_list} */}
            </ul>
            </table>
            </div>
               {/* <table>
                <div class="notif-odd-row">
                    <tr>
                        <td class="notif-info">{this.state.notifications[0]}
                        <a href="#"><div class="button-link">View</div></a>
                        <a href="#"><div class="button-link">Ignore</div></a>
                    </tr>
                </div>
                <div class="notif-even-row">
                    <tr>
                        <td class="notif-info">{this.state.notifications[1]}
                        <a href="#"><div class="button-link">View</div></a>
                        <a href="#"><div class="button-link">Ignore</div></a>
                    </tr>
                </div>
                <div class="notif-odd-row">
                    <tr>
                        <td class="notif-info">{this.state.notifications[2]}
                        <a href="#"><div class="button-link">View</div></a>
                        <a href="#"><div class="button-link">Ignore</div></a>
                    </tr>
                </div>
                <div class="notif-even-row">
                    <tr>
                        <td class="notif-info">{this.state.notifications[3]}
                        <a href="#"><div class="button-link">View</div></a>
                        <a href="#"><div class="button-link">Ignore</div></a>
                    </tr>
                </div>
            </table> */}
            </div>
            
        );
    }
}

export default Notifications;