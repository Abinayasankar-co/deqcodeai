import { ChevronLeftIcon, ChevronRightIcon } from "lucide-react";
import React, { useState, useEffect } from "react";
import ResultDisplay from "./ResultDisplay";
import { Modal } from "react-bootstrap";

const Sidebar = ({ isOpen, toggle, onSelectChat }) => {
  const [currentCircuit, setCurrentCircuit] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const view_template = {
    username: localStorage.getItem("username"),
  };

  useEffect(() => {
    const fetchCircuits = async () => {
      try {
        const response = await fetch("/api/viewcircuits", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(view_template),
        });
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        const data = await response.json();
        if (Array.isArray(data.circuits)) {
          setCurrentCircuit(data.circuits);
        } else {
          console.error("Invalid data format received:", data);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchCircuits();
  }, []);

  const handleChatClick = (chat) => {
    setSelectedChat(chat);
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedChat(null);
  };

  return (
    <div>
      <button
        onClick={toggle}
        className={`fixed top-4 z-20 transition-transform duration-300 bg-orange-500 text-white p-3 
          rounded-full shadow-md hover:bg-orange-600 ${
            isOpen ? "left-60" : "left-4"
          }`}
      >
        {isOpen ? (
          <ChevronLeftIcon className="h-6 w-6" />
        ) : (
          <ChevronRightIcon className="h-6 w-6" />
        )}
      </button>

      <div
        className={`fixed top-0 left-0 h-full w-60 bg-gray-900 text-white shadow-lg transform transition-transform duration-300 ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        <div className="border-b border-gray-700 p-4 text-lg font-bold text-orange-400">
          Chat History
        </div>
        <nav className="flex flex-col overflow-y-auto">
          {currentCircuit.length > 0 ? (
            currentCircuit.map((chat, index) => (
              <button
                key={index}
                onClick={() => handleChatClick(chat)}
                className="block px-4 py-3 border-b border-gray-800 text-lg hover:bg-gray-800 hover:text-orange-300 transition text-left"
              >
                {`Circuits-${index + 1}: ${chat.name ? chat.name : `Unnamed`}`}
              </button>
            ))
          ) : (
            <div className="px-4 py-3 text-gray-500">No Circuits available</div>
          )}
        </nav>
      </div>

      <Modal show={showModal} onHide={handleCloseModal} size="lg" scrollable centered>
        <Modal.Header closeButton>
          <Modal.Title>Chat Details</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {selectedChat && (
            <ResultDisplay
              url={selectedChat.url}
              content={selectedChat.content}
              code={selectedChat.code}
            />
          )}
        </Modal.Body>
      </Modal>
    </div>
  );
};

export default Sidebar;