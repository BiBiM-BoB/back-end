import React from "react";
import JenkinsModal from "./JenkinsModal"
import GitModal from "./GitModal";
import UploadModal from "./UploadModal";
import SaveModal from "./SaveModal";

export default ({
    setModalOpen,
    whichModal,
    setWhichModal
}) => {
    const closeModal = () => {
        setModalOpen(false);
        setWhichModal("");
    }

    switch(whichModal) {
        case "Jenkins" :
            return <JenkinsModal closeModal={closeModal} />
        case "Github" :
            return <GitModal closeModal={closeModal} />
        case "Upload" :
            return <UploadModal closeModal={closeModal} />
        case "Save" :
            return <SaveModal closeModal={closeModal} />
    }
}
