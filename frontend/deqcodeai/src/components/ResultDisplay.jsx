import React from 'react';
import { Card, Container, Row, Col } from 'react-bootstrap';

const ResultDisplay = ({ url, content }) => (
  <Container fluid className="px-4 py-3">
    <Row className="mb-4">
      <Col>
        <Card className="bg-dark border-secondary">
          <Card.Header className="text-warning">Circuit Preview</Card.Header>
          <Card.Body style={{ height: '30vh', minHeight: '300px' }}>
            {url ? (
              <iframe
                src={url}
                className="w-100 h-100"
                title="Circuit Preview"
                style={{ border: 'none', backgroundColor: '#212529' }}
              />
            ) : (
              <div className="d-flex align-items-center justify-content-center h-100 text-light">
                No circuit has been generated yet
              </div>
            )}
          </Card.Body>
        </Card>
      </Col>
    </Row>

    <Row>
      <Col>
        <Card className="bg-dark border-secondary">
          <Card.Header className="text-warning">Circuit Details</Card.Header>
          <Card.Body style={{ height: '20vh', minHeight: '200px', overflowY: 'auto' }}>
            {content ? (
              <p className="text-light mb-0">{content}</p>
            ) : (
              <div className="d-flex align-items-center justify-content-center h-100 text-light">
                No circuit details available
              </div>
            )}
          </Card.Body>
        </Card>
      </Col>
    </Row>
  </Container>
);

export default ResultDisplay;