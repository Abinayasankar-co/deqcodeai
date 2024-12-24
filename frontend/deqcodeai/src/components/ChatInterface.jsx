import { useState } from 'react';
import { Send } from 'lucide-react';

const ChatInterface = ({ onSubmit }) => {
  const [message, setMessage] = useState('');

  return (
    <div className="flex gap-2 p-4 bg-black shadow-md">
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

export default ChatInterface;