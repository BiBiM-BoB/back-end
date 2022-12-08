import React from "react";
import ModalPresenter from "./ModalPresenter";

export default({
   setModalOpen,
   whichModal,
   setWhichModal
}) => {
    return(
        <ModalPresenter
            setModalOpen={setModalOpen}
            whichModal={whichModal}
            setWhichModal={setWhichModal}
        />
    )
}