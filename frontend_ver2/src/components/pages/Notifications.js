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
            songURL: ""
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

    componentDidMount() {
        axios.get(backend_url + "/notifications")
            .then((response) => { 
                console.log(response)               
                this.setState({notifications: response.data.map((p) => p.text)})
                this.setState({type: response.data.map((p) => p.type)})
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

                // if (this.state.type[i] == "NOTIFICATION") {
                //     notification_list.push(
                //         <a href="#"><div class="button-link" onClick={this.shareSong} >View</div></a>
                //     )
                //     notification_list.push(
                //         <a href="#"><div class="button-link">Ignore</div></a>
                //     )
                // } else if (this.state.type[i]  == "FRIEND_REQUEST") {
                //     notification_list.push(
                //         <a href="#"><div class="button-link">Accept</div></a>
                //     )
                //     notification_list.push(
                //         <a href="#"><div class="button-link">Reject</div></a>
                //     )
                // }
                   
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