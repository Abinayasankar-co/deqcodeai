import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthContext';

const Login = () => {
    const {setIsAuthenticated, setUsername} = useAuth();
    const [formData, setFormData] = useState({ username: '', password: '' });
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(()=>{
        localStorage.removeItem('session_token');
        localStorage.removeItem('username');
        setIsAuthenticated(false);
        setUsername('');
    },[setIsAuthenticated, setUsername])

    const handleChange = (e) => {
        const {name, value } = e.target;
        setFormData({ ...formData, [name]: value.trim()});
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
                //navigate('/registration_error');
            }
        } catch (error) {
            console.error('Error:', error);
            setError('An error occurred. Please try again later.');
            navigate('/registration_error');
        }
    };

    return (
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
                            className="w-full p-2 mt-1 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
                            required
                        />
                    </div>
                    {/*Need to write a unique password validation */}
                    <div>
                        <label className="block text-sm font-medium text-gray-300">Password</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            placeholder="Enter your password"
                            className="w-full p-2 mt-1 bg-gray-700 text-white rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500"
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        className="w-full py-2 mt-4 bg-cyan-500 text-orange font-bold rounded-md hover:bg-cyan-600 transition"
                    >
                        Login
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;