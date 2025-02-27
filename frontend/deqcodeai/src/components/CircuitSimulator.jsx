import { useState, useEffect } from 'react';
import { DndProvider, useDrop } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import Gate from './Gate';
import sampleCircuit from '../components/sample.json';

const CircuitSimulator = () => {
  const [circuit, setCircuit] = useState(sampleCircuit);
  const [cache, setCache] = useState({});

  useEffect(() => {
    localStorage.setItem('circuitCache', JSON.stringify(circuit));
    setCache({ ...cache, [JSON.stringify(circuit)]: simulateCircuit(circuit) });
  }, [circuit]);

  const simulateCircuit = (circuitData) => {
    return `Simulated state for ${JSON.stringify(circuitData)}`;
  };

  const addGate = (type, qubit, column) => {
    const newGate = { type, qubit, column };
    if (['CNOT', 'CZ', 'CH', 'CSWAP'].includes(type)) {
      newGate.control = qubit === 0 ? 1 : 0;
    } else if (type === 'CCNOT') {
      newGate.controls = qubit === 0 ? [1, 2] : qubit === 1 ? [0, 2] : [0, 1];
    }
    setCircuit((prev) => ({
      ...prev,
      gates: [...prev.gates.filter(g => g.column !== column || g.qubit !== qubit), newGate],
    }));
  };

  const GridCell = ({ qubit, column }) => {
    const [{ isOver }, drop] = useDrop(() => ({
      accept: 'GATE',
      drop: () => ({ qubit, column }),
      collect: (monitor) => ({
        isOver: monitor.isOver(),
      }),
    }));

    const gate = circuit.gates.find(g => g.qubit === qubit && g.column === column);

    return (
      <div
        ref={drop}
        className={`w-12 h-12 border flex items-center justify-center ${isOver ? 'bg-green-200' : 'bg-white'}`}
      >
        {gate ? (
          gate.control !== undefined ? (
            <div className="flex flex-col items-center">
              <div className="w-2 h-2 bg-black rounded-full"></div>
              <div className="h-6 w-1 bg-black"></div>
              <div className="w-8 h-8 bg-blue-500 text-white flex items-center justify-center rounded">
                {gate.type === 'CNOT' ? 'X' : gate.type === 'CZ' ? 'Z' : gate.type === 'CH' ? 'H' : gate.type === 'CSWAP' ? 'SWAP' : gate.type}
              </div>
            </div>
          ) : gate.controls ? (
            <div className="flex flex-col items-center">
              <div className="w-2 h-2 bg-black rounded-full"></div>
              <div className="h-12 w-1 bg-black"></div>
              <div className="w-8 h-8 bg-blue-500 text-white flex items-center justify-center rounded">
                X
              </div>
            </div>
          ) : (
            <div className="w-8 h-8 bg-blue-500 text-white flex items-center justify-center rounded">
              {gate.type}
            </div>
          )
        ) : null}
      </div>
    );
  };

  const gates = [
    'H', 'X', 'Y', 'Z', 'CNOT', 'S', 'T', 'SWAP', 'CZ',
    'RX', 'RY', 'RZ', 'CH', 'CCNOT', 'CSWAP', 'T†', 'S†'
  ];

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="p-6 bg-white rounded-lg shadow-lg">
        <h1 className="text-2xl font-bold mb-4">Quantum Circuit Simulator</h1>
        <div className="flex flex-wrap gap-4 mb-4">
          {gates.map((gate) => (
            <Gate key={gate} type={gate} onDrop={addGate} />
          ))}
        </div>
        <div className="grid gap-1">
          {Array.from({ length: circuit.qubits }).map((_, qubit) => (
            <div key={qubit} className="flex items-center">
              <span className="w-12 text-center">q{qubit}</span>
              {Array.from({ length: 5 }).map((_, col) => (
                <GridCell key={col} qubit={qubit} column={col} />
              ))}
            </div>
          ))}
        </div>
        <pre className="mt-4 bg-gray-100 p-4 rounded">
          {JSON.stringify(circuit, null, 2)}
        </pre>
        <div className="mt-4">
          <h2 className="text-lg font-semibold">Simulation Output:</h2>
          <p>{cache[JSON.stringify(circuit)] || 'Simulating...'}</p>
        </div>
      </div>
    </DndProvider>
  );
};

export default CircuitSimulator;