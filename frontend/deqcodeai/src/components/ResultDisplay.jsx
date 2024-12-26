import React from 'react';
import { Card, Container, Row, Col } from 'react-bootstrap';

const ResultDisplay = ({ url, content }) => (
  <Container fluid className="px-12 py-3">
    <Row className="mb-4">
      <Col>
      <Card className="w-11/12 max-w-7xl h-[35rem] bg-gray-800 text-white shadow-lg rounded-lg">
        <Card.Header className="text-white"><h1>Circuit Preview</h1></Card.Header>
        <Card.Body className="h-full flex items-center justify-center p-0">
          {url ? (
            <iframe
              src={url}
              title="Circuit Preview"
              className="w-full h-full rounded-lg"
              style={{ border: 'none', backgroundColor: '#212529' }}
            ></iframe>
          ) : (
            <div className="text-center text-lg">
              No circuit has been generated yet
            </div>
          )}
        </Card.Body>
      </Card>
      </Col>
    </Row>

    <Row>
      <Col>
        <Card className="bg-dark border-secondary py-4">
          <Card.Header className="text-white">Circuit Details</Card.Header>
          <Card.Body className="h-full flex items-center justify-center p-0">
            {content ? (
              <p className="text-white mb-0">{content}</p>
              ) : (
              <div className="d-flex align-items-center justify-content-center h-100 text-white">
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