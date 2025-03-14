import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';

const Login = () => {
    const { setIsAuthenticated, setUsername } = useAuth();
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        localStorage.removeItem('session_token');
        localStorage.removeItem('username');
        setIsAuthenticated(false);
        setUsername('');
    }, [setIsAuthenticated, setUsername]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value.trim() });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('session_token', data.session_key);
                localStorage.setItem('username', formData.username);
                setIsAuthenticated(true);
                setUsername(formData.username);
                navigate('/design');
            } else {
                setError('Invalid username or password');
            }
        } catch (error) {
            console.error('Error:', error);
            setError('An error occurred. Please try again later.');
            navigate('/registration_error');
        }
    };

    const handleGoogleSuccess = async (credentialResponse) => {
        try {
            const response = await fetch('/api/googlelogin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ credential: credentialResponse.credential }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('session_token', data.session_key);
                localStorage.setItem('username', data.username);
                setIsAuthenticated(true);
                setUsername(data.username);
                navigate('/design');
            } else {
                setError('Google login failed');
            }
        } catch (error) {
            console.error('Error:', error);
            setError('An error occurred with Google login');
        }
    };

    const handleGoogleError = () => {
        setError('Google login failed');
    };

    return (
        <GoogleOAuthProvider clientId="YOUR_GOOGLE_CLIENT_ID">
            <div className="bg-gray-900 text-white min-h-screen flex items-center justify-center">
                <div className="max-w-md w-full bg-gray-800 p-6 rounded-lg shadow-lg">
                    <h1 className="text-2xl font-bold text-gray-100 text-center mb-6">Login</h1>
                    {error && <p className="text-red-500 text-center mb-4">{error}</p>}
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-300">Username</label>
                            <input
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                                placeholder="Enter your username"
                                className="w-full p-2 mt-1 bg-gray-700 text-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-300">Password</label>
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                                placeholder="Enter your password"
                                className="w-full p-2 mt-1 bg-gray-700 text-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
                                required
                            />
                        </div>
                        <button
                            type="submit"
                            className="w-full py-2 mt-4 bg-cyan-500 text-white font-bold rounded-md hover:bg-cyan-600 transition"
                        >
                            Login
                        </button>
                    </form>
                    <div className="flex items-center my-4">
                        <div className="flex-grow border-t border-gray-600"></div>
                        <span className="mx-4 text-gray-400">or</span>
                        <div className="flex-grow border-t border-gray-600"></div>
                    </div>
                    <div className="flex justify-center">
                        <GoogleLogin
                            onSuccess={handleGoogleSuccess}
                            onError={handleGoogleError}
                            width="300px"
                        />
                    </div>
                </div>
            </div>
        </GoogleOAuthProvider>
    );
};

export default Login;