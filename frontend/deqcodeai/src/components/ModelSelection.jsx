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
import { Badge } from "@/components/ui/badge";
import { 
  Atom, 
  Cpu, 
  Sparkles, 
  Code2, 
  Binary,
  BookOpen,
  Github,
  Globe,
  Coffee,
  Award
} from 'lucide-react';

const FrameworkSelector = ({ onSelect, onClose }) => {
  const [selectedFramework, setSelectedFramework] = useState("");
  const [hoverFeature, setHoverFeature] = useState(null);

  const frameworks = {
    qiskit: {
      name: "Qiskit",
      description: "IBM's comprehensive open-source framework for quantum computing, designed for researchers and developers",
      icon: <Cpu className="w-6 h-6 text-blue-500" />,
      color: "bg-blue-50",
      borderColor: "border-blue-200",
      accentColor: "text-blue-700",
      features: [
        {
          title: "Industry Standard",
          description: "Widely adopted in research and industry",
          icon: <Award className="w-4 h-4" />
        },
        {
          title: "Rich Visualization",
          description: "Advanced circuit visualization and analysis tools",
          icon: <Code2 className="w-4 h-4" />
        },
        {
          title: "IBM Q Integration",
          description: "Direct access to IBM's quantum hardware",
          icon: <Binary className="w-4 h-4" />
        },
        {
          title: "Extensive Documentation",
          description: "Comprehensive tutorials and examples",
          icon: <BookOpen className="w-4 h-4" />
        },
        {
          title: "Active Community",
          description: "Large developer community and support",
          icon: <Github className="w-4 h-4" />
        }
      ],
      metrics: {
        stability: 95,
        performance: 90,
        community: 98
      },
      languageSupport: ["Python", "Julia", "JavaScript"],
      lastUpdate: "2024-02-10"
    },
    cirq: {
      name: "Cirq",
      description: "Google's powerful framework for NISQ algorithms and quantum circuit optimization",
      icon: <Atom className="w-6 h-6 text-green-500" />,
      color: "bg-green-50",
      borderColor: "border-green-200",
      accentColor: "text-green-700",
      features: [
        {
          title: "Clean Syntax",
          description: "Intuitive and pythonic programming model",
          icon: <Code2 className="w-4 h-4" />
        },
        {
          title: "Hardware Optimization",
          description: "Advanced circuit optimization for real hardware",
          icon: <Cpu className="w-4 h-4" />
        },
        {
          title: "Noise Simulation",
          description: "Sophisticated quantum noise modeling",
          icon: <Binary className="w-4 h-4" />
        },
        {
          title: "Cloud Integration",
          description: "Seamless Google Cloud quantum services",
          icon: <Globe className="w-4 h-4" />
        },
        {
          title: "Developer Tools",
          description: "Rich debugging and testing utilities",
          icon: <Coffee className="w-4 h-4" />
        }
      ],
      metrics: {
        stability: 92,
        performance: 95,
        community: 85
      },
      languageSupport: ["Python", "C++"],
      lastUpdate: "2024-02-01"
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 text-white">
      <Card className="w-full max-w-2xl">
        <CardHeader className="border-b">
          <div className="flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-purple-500" />
            <CardTitle>Quantum Framework Selection</CardTitle>
          </div>
          <CardDescription>
            Choose a quantum computing framework to power your quantum applications
          </CardDescription>
        </CardHeader>
        
        <CardContent className="space-y-6 pt-6">
          <Select
            value={selectedFramework}
            onValueChange={setSelectedFramework}
          >
            <SelectTrigger className="w-full">
              <SelectValue placeholder="Select your preferred framework" />
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
            <div className={`rounded-lg ${frameworks[selectedFramework].color} ${frameworks[selectedFramework].borderColor} border overflow-hidden`}>
              <div className="p-4 border-b border-opacity-50">
                <div className="flex items-center gap-2 mb-3">
                  {frameworks[selectedFramework].icon}
                  <h3 className="font-semibold text-lg">
                    {frameworks[selectedFramework].name}
                  </h3>
                </div>
                <p className={`${frameworks[selectedFramework].accentColor}`}>
                  {frameworks[selectedFramework].description}
                </p>
              </div>
              
              <div className="p-4 space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {frameworks[selectedFramework].features.map((feature, index) => (
                    <div
                      key={index}
                      className="flex items-start gap-3 p-3 rounded-md bg-white/60 hover:bg-white/90 transition-colors cursor-pointer"
                      onMouseEnter={() => setHoverFeature(index)}
                      onMouseLeave={() => setHoverFeature(null)}
                    >
                      <div className={`mt-1 ${hoverFeature === index ? 'text-purple-500' : frameworks[selectedFramework].accentColor}`}>
                        {feature.icon}
                      </div>
                      <div>
                        <h4 className="font-medium">{feature.title}</h4>
                        <p className="text-sm text-gray-600">{feature.description}</p>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="flex flex-wrap gap-2 items-center">
                  <span className="text-sm text-gray-600">Supported Languages:</span>
                  {frameworks[selectedFramework].languageSupport.map((lang) => (
                    <Badge key={lang} variant="secondary">{lang}</Badge>
                  ))}
                </div>

                <div className="grid grid-cols-3 gap-4">
                  {Object.entries(frameworks[selectedFramework].metrics).map(([key, value]) => (
                    <div key={key} className="text-center p-2 bg-white/60 rounded-lg">
                      <div className="text-sm text-gray-600 capitalize mb-1">{key}</div>
                      <div className="font-semibold text-lg">{value}%</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </CardContent>

        <CardFooter className="flex justify-between border-t p-4">
          <div className="text-sm text-gray-500">
            {selectedFramework && `Last updated: ${frameworks[selectedFramework].lastUpdate}`}
          </div>
          <div className="flex gap-3">
            <Button variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button
              onClick={() => onSelect(selectedFramework)}
              disabled={!selectedFramework}
              className="bg-purple-600 hover:bg-purple-700"
            >
              Select Framework
            </Button>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
};

export default FrameworkSelector;