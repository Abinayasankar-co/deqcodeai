import React, { useState } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import ChatInterface from './ChatInterface';
import ResultDisplay from './ResultDisplay';

const Main = ({ email }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [messages, setMessages] = useState([]);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (message) => {
    setMessages([...messages, message]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/design', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error(error);
    }

    setIsLoading(false);
  };

  return (
    <>
    <Container fluid className="vh-100 p-0 bg-black">
      <Navbar email={email} />
      <Row className="h-100 g-0">
        <Sidebar
          isOpen={sidebarOpen}
          toggle={() => setSidebarOpen(!sidebarOpen)}
          chats={[{ title: 'Previous Chat 1' }, { title: 'Previous Chat 2' }]}
        />
        <Col
          className="h-100 d-flex flex-column"
          style={{
            marginLeft: sidebarOpen ? '250px' : '0',
            transition: 'margin-left 0.3s ease-in-out',
          }}
        >
          <ChatInterface onSubmit={handleSubmit} />
          <div className="flex-1 overflow-auto p-4">
            {result && <ResultDisplay url={result.url} content={result.content} />}
          </div>
        </Col>
      </Row>
    </Container>
    </>
  );
};

export default Main;