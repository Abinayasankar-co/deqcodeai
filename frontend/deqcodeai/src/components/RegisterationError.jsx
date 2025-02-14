import React from 'react';
import Footer from '../components/Footer';
import { useNavigate } from 'react-router-dom';

const RegistrationError = () => {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-white">
      <div className="flex-grow flex flex-col justify-center items-center">
        <h1 className="text-4xl font-bold mb-4">Registration Error</h1>
        <p className="text-lg text-gray-300 mb-6">We encountered an issue with your registration.Please try again later.</p>
        <button
          onClick={() => navigate('/register')}
          className="px-4 py-2 bg-cyan-500 rounded hover:bg-cyan-600 transition"
        >
          Go to Register Page
        </button>
      </div>
      <Footer />
    </div>
  );
};

export default RegistrationError;
