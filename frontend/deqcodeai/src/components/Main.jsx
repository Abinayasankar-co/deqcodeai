import { useState, useEffect } from 'react';
import { Menu, X, Send, ChevronLeft, ChevronRight } from 'lucide-react';

const Navbar = ({ email }) => (
  <nav className="bg-gray-900 text-white p-4 flex justify-between items-center">
    <h1 className="text-xl font-bold">Circuit Designer</h1>
    <span className="text-orange-400">{email}</span>
  </nav>
);

const Sidebar = ({ isOpen, toggle, chats }) => (
  <aside 
    className={`fixed top-16 left-0 h-full bg-gray-800 shadow-lg transition-all duration-300 overflow-hidden ${isOpen ? 'w-64' : 'w-0'}`}
  >
    <button 
      onClick={toggle} 
      className="absolute -right-10 top-4 bg-orange-500 p-2 rounded-r text-white"
    >
      {isOpen ? <ChevronLeft /> : <ChevronRight />}
    </button>
    <div className="py-4">
      {chats.map((chat, i) => (
        <div key={i} className="px-4 py-2 hover:bg-gray-700 text-white cursor-pointer">
          {chat.title}
        </div>
      ))}
    </div>
  </aside>
);

const ChatInterface = ({ onSubmit }) => {
  const [message, setMessage] = useState('');
  
  return (
    <div className="flex gap-2 p-4 bg-gray-800 shadow-md">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        className="flex-1 p-2 border rounded bg-gray-700 text-white border-gray-600"
        placeholder="Type your message..."
      />
      <button
        onClick={() => {
          onSubmit(message);
          setMessage('');
        }}
        className="bg-orange-500 text-white px-4 py-2 rounded hover:bg-orange-600"
      >
        <Send size={20} />
      </button>
    </div>
  );
};

const MessageDisplay = ({ message }) => (
  <div className="p-4 bg-gray-700 text-white rounded-lg mb-4">
    {message}
  </div>
);

const ResultDisplay = ({ url, content }) => (
  <div className="grid grid-rows-2 gap-4 p-4">
    <div className="w-full h-full border rounded bg-gray-700 text-white">
      {url ? (
        <iframe src={url} className="w-full h-full" />
      ) : (
        <div className="flex items-center justify-center h-full">
          No URL Results Available
        </div>
      )}
    </div>
    <div className="bg-gray-700 p-4 rounded text-white">
      {content || "No Content Available"}
    </div>
  </div>
);

const Spinner = () => (
  <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
    <div className="bg-gray-800 p-6 rounded-lg shadow-xl text-center">
      <div className="animate-spin rounded-full h-12 w-12 border-4 border-orange-500 border-t-transparent mx-auto mb-4"></div>
      <p className="text-lg font-semibold text-white">The Circuit is Preparing...</p>
    </div>
  </div>
);

const MainPage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [result, setResult] = useState(null);
  const [email, setEmail] = useState('');
  const [messages, setMessages] = useState([]);

  const handleSubmit = async (message) => {
    setIsLoading(true);
    setMessages([...messages, message]);
    try {
      const response = await fetch('your-api-endpoint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      const data = await response.json();
      setResult(data);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gray-900">
      <Navbar email={email} />
      <div className="flex-1 flex relative">
        <Sidebar
          isOpen={sidebarOpen}
          toggle={() => setSidebarOpen(!sidebarOpen)}
          chats={[{ title: 'Previous Chat 1' }, { title: 'Previous Chat 2' }]}
        />
        <div className={`flex-1 flex flex-col transition-all ${sidebarOpen ? 'ml-64' : ''}`}>
          <ChatInterface onSubmit={handleSubmit} />
          <div className="flex-1 overflow-auto">
            {messages.map((msg, i) => (
              <MessageDisplay key={i} message={msg} />
            ))}
            {result && <ResultDisplay url={result.url} content={result.content} />}
          </div>
        </div>
      </div>
      {isLoading && <Spinner />}
    </div>
  );
};

export default MainPage;