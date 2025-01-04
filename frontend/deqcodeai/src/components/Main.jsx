import React, { useState, useEffect } from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import Spinner from './Spinner';
import ResultDisplay from './ResultDisplay';
import ChatInterface from './ChatInterface';
import { useNavigate } from 'react-router-dom';

const Main = () => {
  const [currentCircuit, setCurrentCircuit] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [messages, setMessages] = useState([]);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const navigate  = useNavigate();
  
  const view_template = {
    "username": localStorage.getItem('username')
  }
  useEffect(() => {
      try{
        fetch('/api/viewcircuits',{
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(view_template)
          })
          .then((response) => response.json())
          .then((data) => localStorage.setItem('circuits', JSON.stringify(data)))
          .catch((error) => console.error('Error fetching data:', error));

      }catch{
          console.error('Error fetching data');
      }
    },
  [])

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
          navigate('/error');
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data) //Ref
        setResult(data);
      },1000)
      if(data.error){
        navigate('/error');
      }
    } catch (error) {
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
        <Sidebar
          isOpen={sidebarOpen}
          toggle={() => setSidebarOpen(!sidebarOpen)}
          //chats = {localStorage.getItem('circuits')}
          chats = {localStorage.getItem('circuits')}
          setCurrentCircuit={setCurrentCircuit}
          //chats={[{ title: 'Previous Chat 1' }, { title: 'Previous Chat 2' }]}
        />
        <Col
          className="h-100 d-flex flex-column"
          style={{
            marginLeft: sidebarOpen ? '250px' : '0',
            transition: 'margin-left 0.3s ease-in-out',
          }}
        >
          <ChatInterface onSubmit={handleSubmit} />
          {isLoading && <Spinner/>}
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