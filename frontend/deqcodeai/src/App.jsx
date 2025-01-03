import MainPage from './components/Main'
import {Route,Routes} from 'react-router-dom'
import './index.css'
import Registration from './components/Registeration'
import RegistrationError from './components/RegisterationError'
import OtherError from './components/OtherError'
import NotFound404 from './components/NotFoundError'
import Login from './components/login'
import { AuthProvider, useAuth } from './AuthContext';
import { Navigate } from 'react-router-dom';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) {
    return <Navigate to="/design"/>;
  }
  return children;
};

function App() {
  return (
    <AuthProvider>
     <Routes>
      <Route 
           path="/design" 
           element={
            <ProtectedRoute>
              <MainPage />
            </ProtectedRoute>
            } 
      />
      <Route path='/register' element={<Registration/>}/>
      <Route path='/registration_error' element={<RegistrationError/>}/>
      <Route path='/error' element={<OtherError/>}/>
      <Route path='/canthandle' element={<NotFound404/>}/>
      <Route path='/login' element={<Login/>}/>
      <Route path="*" element={<Login/>}/> {/*The Landing page is to be redirected*/}
     </Routes>
     </AuthProvider>
  )
}

export default App
