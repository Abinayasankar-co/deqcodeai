import React from 'react';
import { useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Atom, Cpu, Sparkles } from 'lucide-react';

const FrameworkSelector = ({ onSelect, onClose }) => {
  const [selectedFramework, setSelectedFramework] = useState("");

  const frameworks = {
    qiskit: {
      name: "Qiskit",
      description: "IBM's open-source framework for quantum computing",
      icon: <Cpu className="w-6 h-6 text-blue-500" />,
      color: "bg-blue-50",
      borderColor: "border-blue-200",
      features: ["Industry standard", "Rich visualization", "IBM Q integration"]
    },
    cirq: {
      name: "Cirq",
      description: "Google's framework for NISQ algorithms",
      icon: <Atom className="w-6 h-6 text-green-500" />,
      color: "bg-green-50",
      borderColor: "border-green-200",
      features: ["Clean syntax", "Hardware-aware circuits", "Quantum noise simulation"]
    }
  };

  const handleSelect = () => {
    if (selectedFramework) {
      onSelect(selectedFramework);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4">
      <Card className="w-full max-w-xl">
        <CardHeader>
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-purple-500" />
            <CardTitle>Choose Your Quantum Framework</CardTitle>
          </div>
          <CardDescription>
            Select the quantum computing framework that best suits your needs
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-6">
          <Select
            value={selectedFramework}
            onValueChange={setSelectedFramework}
          >
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Select a framework" />
            </SelectTrigger>
            <SelectContent>
              {Object.entries(frameworks).map(([key, framework]) => (
                <SelectItem key={key} value={key}>
                  <div className="flex items-center gap-2">
                    {framework.icon}
                    <span>{framework.name}</span>
                  </div>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {selectedFramework && (
            <div className={`p-4 rounded-lg ${frameworks[selectedFramework].color} ${frameworks[selectedFramework].borderColor} border`}>
              <div className="flex items-center gap-2 mb-3">
                {frameworks[selectedFramework].icon}
                <h3 className="font-semibold text-lg">
                  {frameworks[selectedFramework].name}
                </h3>
              </div>
              <p className="text-gray-600 mb-4">
                {frameworks[selectedFramework].description}
              </p>
              <div className="space-y-2">
                {frameworks[selectedFramework].features.map((feature, index) => (
                  <div key={index} className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-gray-400" />
                    <span className="text-sm text-gray-600">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>

        <CardFooter className="flex justify-end gap-3">
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button
            onClick={handleSelect}
            disabled={!selectedFramework}
            className="bg-purple-600 hover:bg-purple-700"
          >
            Select Framework
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default FrameworkSelector;