import React from 'react';
import Footer from '../components/Footer';
import { useNavigate } from 'react-router-dom';

const OtherError = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-white">
      <div className="flex-grow flex flex-col justify-center items-center">
        <h1 className="text-4xl font-bold mb-4">Error</h1>
        <p className="text-lg text-gray-300 mb-6">An unexpected error occurred. Please try again later.</p>
        <button
          onClick={() => navigate('/design')}
          className="px-4 py-2 bg-cyan-500 rounded hover:bg-cyan-600 transition"
        >
          Go to Design Page
        </button>
      </div>
      <Footer />
    </div>
  );
};

export default OtherError;
