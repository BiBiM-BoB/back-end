import React from "react";
import styled from "styled-components";

const ModalDiv = styled.div`
    position: absolute;
    top: 0;
    left: 0;
    width: 110vw;
    height: 110vh;
    background: rgba(0, 0, 0, 0.5)
`;

const Modal = styled.div`
    /* 모달창 크기 */
    width: 300px;
    height: 200px;
    
    /* 최상단 위치 */
    z-index: 999;
    
    /* 중앙 배치 */
    /* top, bottom, left, right 는 브라우저 기준으로 작동한다. */
    /* translate는 본인의 크기 기준으로 작동한다. */
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    
    /* 모달창 디자인 */
    background-color: rgba(0, 0, 0, 0.69);
    border-radius:3px;
`;

const CloseButton = styled.button`
    position: absolute;
    right: 10px;
    top: 10px;
`;

export default ({
                    closeModal
                }) => {
    return (
        <ModalDiv>
            <Modal>
                <CloseButton onClick={closeModal}>
                    X
                </CloseButton>
                <p>깃 모달창입니다.</p>
            </Modal>
        </ModalDiv>
    );
}