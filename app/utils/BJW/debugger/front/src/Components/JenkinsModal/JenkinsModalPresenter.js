import React from "react";

export default ({
    dummy
}) => {
    return (
        <JenkinsModal>
            <CloseButton>

            </CloseButton>
            <JenkinsFormDiv>
                <JenkinsForm>
                    <InputDiv>
                        <Label>Jenkins Server URL</Label>
                        <Input name="url" />
                    </InputDiv>
                    <InputDiv>
                        <Label>Jenkins Username</Label>
                        <Input name="username" />
                    </InputDiv>
                    <InputDiv>
                        <Label>Jenkins Token(Password)</Label>
                        <Input name="token" type="password" />
                    </InputDiv>
                </JenkinsForm>
            </JenkinsFormDiv>
        </JenkinsModal>
    )
}