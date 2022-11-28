import React, {useState} from "react";
import styled from "styled-components";
import Button from "../Components/Button"
import Editor from "../Components/Editor"
import SideButton from "../Components/SideButton";
import {Git, Jenkins, Save} from "../Assets"

const SideButtonDiv = styled.div`
    position: fixed;
`;

export default ({
    temp
}) => {

    return (
        <SideButtonDiv>
            <SideButton
                image={Jenkins}
                value={"Jenkins"}
            />
            <SideButton
                image={Git}
                value={"Github"}
            />
            <SideButton
                image={Save}
                value={"Push!"}
            />
        </SideButtonDiv>
    )
}