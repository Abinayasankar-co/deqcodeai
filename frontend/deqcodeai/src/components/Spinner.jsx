import { Spinner as BootstrapSpinner } from 'react-bootstrap';

const Spinner = () => (
  <div 
    className="position-fixed top-0 start-0 w-100 h-100 bg-dark d-flex align-items-center justify-content-center"
    //style={{ zIndex: 1050, backgroundColor: 'rgba(0, 0, 0, 0.9)' }}
  >
    <div className="bg-dark p-4 rounded text-center">
      <BootstrapSpinner
        animation="border"
        variant="warning"
        style={{ width: '3rem', height: '3rem' }}
      />
      <p className="mt-3 text-lg fs-5 fw-semibold">
        The Circuit is Preparing...
      </p>
    </div>
  </div>
);

export default Spinner;