import React from "react";
import CodeMirror from "@uiw/react-codemirror";
import { StreamLanguage } from '@codemirror/language';
import { groovy } from "@codemirror/legacy-modes/mode/groovy";
import { sublime } from "@uiw/codemirror-theme-sublime";

export default ({
    code,
    height
}) => {
    return (
        <CodeMirror
            value={code}
            height={height}
            theme={sublime}
            extensions={[StreamLanguage.define(groovy)]}
        />
    )
}