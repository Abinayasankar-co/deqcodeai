import React, { useState, useEffect } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import Navbar from './Navbar';
import Spinner from './Spinner';
import Sidebar from "./Sidebar";
import ResultDisplay from './ResultDisplay';
import ChatInterface from './ChatInterface';
import { useNavigate } from 'react-router-dom';

const Main = () => {
  const [sidebar, setSidebar] = useState(false);
  const [messages, setMessages] = useState([]);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (message) => {
    setMessages([...messages, message]);
    const statements = {
      'username': localStorage.getItem('username'),
      'statements': message
    }
    try {
      setTimeout(async () => {
        setIsLoading(true);
        console.log(statements); //Ref
        const response = await fetch('/api/design-circuit', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(statements),
        });
        if (!response.ok) {
          setIsLoading(false);
          navigate('/error');
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data) //Ref
        setIsLoading(false);
        setResult(data);
      }, 1000)
      if (data.error) {
        setIsLoading(false);
        navigate('/error');
      }
    } catch (error) {
      setIsLoading(false);
      console.error(error);
      //navigate('/error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Container fluid className="vh-100 p-0 bg-black">
        <Navbar username={localStorage.getItem('username')} />
        <Row className="h-100 g-0">
          <Sidebar isOpen={sidebar} toggle={() => setSidebar(!sidebar)} />
          <Col
            className="h-100 d-flex flex-column"
            style={{
              marginLeft: sidebar ? '15rem' : '0',
              transition: 'margin-left 0.3s ease-in-out',
            }}
          >
            <ChatInterface onSubmit={handleSubmit} />
            {isLoading && <Spinner />}
            <div className="flex-1 overflow-auto p-4">
              {result && <ResultDisplay url={result.url} content={result.content} code={result.code} />}
            </div>
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Main;