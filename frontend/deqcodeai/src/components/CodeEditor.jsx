import React, { useState } from 'react';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-monokai';

const CodeEditor = () => {
  const [code, setCode] = useState('# Quantum code editor for Qiskit and Cirq');

  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  const handleSubmit = async () => {
    setOutput(''); 
    try {
      const response = await fetch('/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
      const data = await response.json();
      setOutput(data.result);
    } catch (error) {
      setOutput(`Error: ${error.message}`);
    } finally {
      setIsProcessing(false); 
    }
  };

  return (
    <div className="flex flex-col h-[40rem] w-full">
      <div className="flex-grow">
        <AceEditor
          mode="python"
          theme="monokai"
          name="quantum_code_editor"
          value={code}
          onChange={handleCodeChange}
          editorProps={{ $blockScrolling: true }}
          width="100%"
          height="100%"
          fontSize={16}
          wrapEnabled={true}
          showPrintMargin={true}
          highlightActiveLine={true}
          setOptions={{
            enableBasicAutocompletion: true,
            enableLiveAutocompletion: true,
            enableSnippets: true,
            showLineNumbers: true,
            tabSize: 4,
          }}
          className="border-2 border-gray-700 rounded-md"
        />
      </div>
      <button
        onClick={handleSubmit}
        className="mt-4 bg-blue-600 text-white py-3 px-5 rounded-lg hover:bg-blue-700 transition"
      >
        Execute
      </button>
    </div>
  );
};

export default CodeEditor;
