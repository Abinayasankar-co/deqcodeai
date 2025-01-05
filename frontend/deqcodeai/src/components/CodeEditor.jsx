import React, { useState } from 'react';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-monokai';

const CodeEditor = ({ onExecute }) => {
  const [code, setCode] = useState('// Write your quantum code here...');

  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  return (
    <div className="flex flex-col h-[35rem] w-full">
      <div className="flex-grow">
        <AceEditor
          mode="python" // Qiskit and Cirq are Python-based
          theme="monokai"
          name="code_editor"
          value={code}
          onChange={handleCodeChange}
          editorProps={{ $blockScrolling: true }}
          width="100%"
          height="100%"
          fontSize={14}
          wrapEnabled={true}
          showPrintMargin={false}
          highlightActiveLine={true}
          setOptions={{
            enableBasicAutocompletion: true,
            enableLiveAutocompletion: true,
            enableSnippets: true,
          }}
          className="border-2 border-gray-700 rounded-lg"
        />
      </div>
      <button
        onClick={() => onExecute(code)}
        className="mt-4 bg-orange-500 text-white py-2 px-4 rounded-lg shadow hover:bg-orange-600"
      >
        Execute
      </button>
    </div>
  );
};

export default CodeEditor;
