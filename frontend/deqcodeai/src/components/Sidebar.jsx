import { Offcanvas, Nav, Button } from 'react-bootstrap';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const Sidebar = ({ isOpen, toggle, chats }) => {
  return (
    <>
      <Button
        onClick={toggle}
        variant="warning"
        className="position-fixed"
        style={{
          left: isOpen ? '240px' : '0',
          top: '1rem',
          zIndex: 1031,
          transition: 'left 0.3s ease-in-out',
          backgroundColor: '#FF7F11',
          border: 'none',
        }}
      >
        {isOpen ? <ChevronLeft size={24} /> : <ChevronRight size={24} />}
      </Button>

      <Offcanvas
        show={isOpen}
        onHide={toggle}
        backdrop={false}
        scroll={true}
        style={{
          width: '250px',
          backgroundColor: '#000',
          color: '#fff',
        }}
      >
        <Offcanvas.Header className="border-bottom border-secondary">
          <Offcanvas.Title className="text-warning">Chat History</Offcanvas.Title>
        </Offcanvas.Header>

        <Offcanvas.Body className="p-0">
          <Nav className="flex-column">
            {chats.map((chat, index) => (
              <Nav.Link
                key={index}
                className="text-light px-3 py-2 border-bottom border-secondary"
                href={`#chat-${index}`}
                style={{
                  backgroundColor: '#000',
                }}
              >
                {chat.title}
              </Nav.Link>
            ))}
          </Nav>
        </Offcanvas.Body>
      </Offcanvas>
    </>
  );
};

export default Sidebar;