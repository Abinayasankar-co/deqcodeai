//import { useState,useEffect} from "react";  // Need When we fetch the data and we display them 
import { ChevronLeftIcon, ChevronRightIcon } from "lucide-react";

const Sidebar = ({ isOpen, toggle,chats}) => {
   //const [chats, setChats] = useState({});
  //setTimeout(async() => {},1000);

  return (
    <div>
      <button
        onClick={toggle}
        className={`fixed top-4 z-20 transition-transform duration-300 bg-orange-500 text-white p-3 rounded-full shadow-md hover:bg-orange-600 ${
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
          Circuit Design History
        </div>
        <nav className="flex flex-col">
          {chats.map((chat, index) => (
            <a
              key={index}
              href={`#chat-${index}`}
              className="block px-4 py-3 border-b border-gray-800 hover:bg-gray-800 hover:text-orange-300 transition"
            >
              {chat.title}
            </a>
          ))}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;