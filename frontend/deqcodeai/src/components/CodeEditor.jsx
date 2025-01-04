import React, { useState } from 'react';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-monokai';

const CodeEditor = () => {
  const [code, setCode] = useState('Your Quantum code is Displayed here');

  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  return (
    <div className="code-editor-container">
      <h2>Quantum Code Editor</h2>
      <AceEditor
        mode="python" 
        theme="monokai"
        name="code_editor"
        value={code}
        onChange={handleCodeChange}
        editorProps={{ $blockScrolling: true }}
        width="100%"
        height="400px"
        fontSize={14}
        wrapEnabled={true}
        showPrintMargin={false}
        highlightActiveLine={true}
        setOptions={{
          enableBasicAutocompletion: true,
          enableLiveAutocompletion: true,
          enableSnippets: true,
        }}
      />
      <button onClick={() => alert('Running code: \n' + code)}>Run Code</button>
    </div>
  );
};

export default CodeEditor;
