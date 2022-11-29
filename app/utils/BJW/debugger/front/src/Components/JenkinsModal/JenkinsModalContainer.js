import React, { Component } from 'react';
import JenkinsModalPresenter from "./JenkinsModalPresenter";
import TriggerButton from "./TriggerButton";

export class Container extends Component {
    state = { isShown: false };

    showModal = () => {
        this.setState({ isShown: true }, () => {
            this.closeButton.focus();
        });
        this.toggleScrollLock();
    };

    closeModal = () => {
        this.setState({ isShown: false });
    }
}

export default Container;