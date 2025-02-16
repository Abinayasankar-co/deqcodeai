import React, { useState,useEffect } from 'react';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-monokai';
import FrameworkSelector from './ModelSelection';

const CodeEditor = ({codeList}) => {
  const [code, setCode] = useState(codeList.join('\n'));
  const [model,setModel] = useState('');
  const [modelCardDisplay,setModelCardDisplay] = useState(false); 
  const[output,setOutput] = useState('');

  useEffect(() => {
    setCode(codeList.join('\n'));
  }, [codeList]);

  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  const processCodeToList = (codeString) => {
    return codeString
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0);
  };

  const handleSubmit = async () => {
    setOutput(''); 
    setModelCardDisplay(true);
    const codeList = processCodeToList(code);
    try {
      setModelCardDisplay(false);
      const response = await fetch('/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          code : codeList,

         }),
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
      {modelCardDisplay && <FrameworkSelector/>}
    
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
