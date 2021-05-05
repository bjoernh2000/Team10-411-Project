import React, { Component } from 'react';
import { axios, backend_url } from '../../App.js';
import './Notifications.css';
import { Text, Linking } from 'react-native';



export class Notifications extends Component {

    constructor(props) {
        super(props)

        this.state = {
            notifications: [],
            user: "",
            friend: "",
            type: null
        }
    }

    componentDidMount() {
        axios.get(backend_url + "/notifications")
            .then((response) => {
                console.log(response);

                this.setState({notifications: response.data.map((p) => p.text)})
                this.setState({type: response.data.type.map((p) => p.text)})
                console.log(response.data.type.map());
            })
            .catch((error) => {
                console.log(error);
            })
    }

    render() {
        const { notifications } = this.state
        const notification_list = []
        for (let i = 0; i < this.state.notifications.length; i++) {
            if (i %2 == 0) {
                notification_list.push(
                <li className='even-notif'>
                <h2>
                    {this.state.notifications[i]}
                </h2>
            </li> )
            } else {
            notification_list.push(
                <li className='notif-item'>
                    <h2>
                        {this.state.notifications[i]}
                    </h2>
                </li>
            )
            }
        }





        return (
            <div>
            <header>
               <h1>BAD DJ ­-  Notifications</h1>
            </header>
            <div class="notif-row">
            <ul>
            {notification_list}
            </ul>
            </div>
               {/* <table>
                <div class="notif-odd-row">
                    <tr>
                        <td class="notif-info">{this.state.notifications[0]}</td>
                        <td><a href="#"><div class="button-link">View</div></a></td>
                        <td><a href="#"><div class="button-link">Ignore</div></a></td>
                    </tr>
                </div>
                <div class="notif-even-row">
                    <tr>
                        <td class="notif-info">{this.state.notifications[1]}</td>
                        <td><a href="#"><div class="button-link">View</div></a></td>
                        <td><a href="#"><div class="button-link">Ignore</div></a></td>
                    </tr>
                </div>
                <div class="notif-odd-row">
                    <tr>
                        <td class="notif-info">{this.state.notifications[2]}</td>
                        <td><a href="#"><div class="button-link">View</div></a></td>
                        <td><a href="#"><div class="button-link">Ignore</div></a></td>
                    </tr>
                </div>
                <div class="notif-even-row">
                    <tr>
                        <td class="notif-info">{this.state.notifications[3]}</td>
                        <td><a href="#"><div class="button-link">View</div></a></td>
                        <td><a href="#"><div class="button-link">Ignore</div></a></td>
                    </tr>
                </div>
            </table> */}
            </div>
        );
    }
}

export default Notifications;