import React, {useState} from "react";
import styled from "styled-components";
import Button from "../Components/Button"
import Editor from "../Components/Editor"
import Modal from "../Modal"
import SideButton from "../Components/SideButton";
import {Git, Jenkins, Save} from "../Assets"

const DebuggerDiv = styled.div`

`;

const MainDiv = styled.div`
    margin-left: 80px;
    margin-right: 10px;
    
    left: 0;
    right: 0;
    
    min-height: 90vh;
    padding: 5vh;
    
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-evenly;
`;

const SideButtonDiv = styled.div`
    position: fixed;
    margin: auto;
    width: 80px;
`;

const BuildDiv = styled.div`
    width: 90%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
`;

const StatusDiv = styled.div`
    margin: auto;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    width: 95%;
`;

const ButtonDiv = styled.div`
    width: auto;
    height: auto;
    margin: 0;
    padding: 0;
    
    display: flex;
    flex-direction: row;
    align-items: center;
`;

const BuildButton = styled.button`
    margin-right: 10px;

    padding: 0;
    box-sizing: border-box;
    height: 20px;
    width: 20px;
    border-style: solid;
    border-width: 10px 0px 10px 20px;
    border-color: white white white green;
    
    &:hover {
        border-color: white white white #404040;
    }
`;

export default ({
    temp
}) => {
    const [modalOpen, setModalOpen] = useState(false);
    const [whichModal, setWhichModal] = useState(""); //현재 열려있는 모달이 어떤 모달인지 저장

    const showModal = (modalName, e) => {
        setModalOpen(true);
        setWhichModal(modalName);
        e.preventDefault();
    }

    return (
        <DebuggerDiv>
            <SideButtonDiv>
                <SideButton
                    image={Jenkins}
                    value={"Jenkins"}
                    showModal={showModal}
                />
                <SideButton
                    image={Git}
                    value={"Github"}
                    showModal={showModal}
                />
                <SideButton
                    image={Save}
                    value={"Save"}
                    showModal={showModal}
                />
            </SideButtonDiv>
            <MainDiv>
                {modalOpen &&
                    <Modal
                        setModalOpen={setModalOpen}
                        whichModal={whichModal}
                        setWhichModal={setWhichModal} // 닫기 버튼 or 외부 클릭시 빈 문자열로 whichModal 초기화
                    />
                }
                <Editor
                    code={"Hello World"}
                />
                <BuildDiv>
                    <StatusDiv>
                        <ButtonDiv>
                            <BuildButton />
                            <p>Build URL:</p>
                        </ButtonDiv>
                    </StatusDiv>
                </BuildDiv>
            </MainDiv>
        </DebuggerDiv>
    )
}