import React, {useState} from "react";
import styled from "styled-components";
import Button from "../Components/Button"
import Editor from "../Components/Editor"
import SideButton from "../Components/SideButton";
import {Git, Jenkins, Save} from "../Assets"

const DebuggerDiv = styled.div`
    display: flex;
    position: relative;
`;

const SideButtonDiv = styled.div`
    position: fixed;
`;

const EditorDiv = styled.div`
    width: 60vw;
    margin: 0 auto;
    margin-top: 20vh;
`;

export default ({
    temp
}) => {

    return (
        <DebuggerDiv>
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
            <EditorDiv>
                <Editor
                    code={"test"}
                    height={"20vw"}
                />
            </EditorDiv>
        </DebuggerDiv>
    )
}