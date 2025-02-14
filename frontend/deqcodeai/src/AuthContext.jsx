import { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [username, setUsername] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem('session_token');
        if (token) {
            setIsAuthenticated(true);
            setUsername(localStorage.getItem('username'));
        }
        setLoading(false); 
    }, []);

    if (loading) {
        return <div>Loading.....</div>; 
    }

    return (
        <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated, username, setUsername }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};