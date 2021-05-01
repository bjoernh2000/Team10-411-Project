import React from 'react';
import './Notifications.css';
export default function Notifications() {
    return (
        <>
        <header>
            <h1>BAD DJ ­-  Notifications</h1>
        </header>
        <div class="main">
            <table>
                <div class="notif-odd-row">
                    <tr>
                        <td class="notif-info">Adam has sent you a friend
                                request.</td>
                        <td><a href="#"><div class="button-link">Accept</div></a></td>
                        <td><a href="#"><div class="button-link">Reject</div></a></td>
                    </tr>
                </div>
                <div class="notif-even-row">
                    <tr>
                        <td class="notif-info">Della has commented on your playlist.</td>
                        <td><a href="#"><div class="button-link">View</div></a></td>
                        <td><a href="#"><div class="button-link">Ignore</div></a></td>
                    </tr>
                </div>
            </table>
        </div>
        </>
    );
}