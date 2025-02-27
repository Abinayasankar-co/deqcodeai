import React, { useState, useEffect } from 'react';
import AceEditor from 'react-ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-monokai';
import FrameworkSelector from './ModelSelection';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';

const CodeEditor = ({ codeList }) => {
  const [code, setCode] = useState(codeList.join('\n'));
  const [simulator, setSimulator] = useState('qiskit');
  const [modelCardDisplay, setModelCardDisplay] = useState(false);
  const [output, setOutput] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    setCode(codeList.join('\n'));
  }, [codeList]);

  const handleCodeChange = (newCode) => {
    setCode(newCode);
  };

  const handleSubmit = async () => {
    setOutput(null);
    setModelCardDisplay(true);
    setIsProcessing(true);
    try {
      setModelCardDisplay(false);
      console.log(simulator);
      const response = await fetch('/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          code: code,
          simulator: simulator,
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
      {modelCardDisplay && <FrameworkSelector />}
      <OverlayTrigger
        placement='Top'
        overlay={
          <Tooltip id="button-tooltip">
             The Generated output is just a simulator response not a original Quantum computer code
          </Tooltip>
        }
      >
      <button
        onClick={handleSubmit}
        className="mt-4 bg-blue-600 text-white py-3 px-5 rounded-lg hover:bg-blue-700 transition"
      >
        Execute
      </button>
      </OverlayTrigger>
      {output && (
        <div className="mt-4">
          <pre className="bg-gray-100 text-black text-bold p-4 rounded-md">{JSON.stringify(output, null, 2)}</pre>
          {output.resultmap && (
            <img src={`data:image/png;base64,${output.resultmap}`} alt="Histogram" />
          )}
        </div>
      )}
    </div>
  );
};

export default CodeEditor;
