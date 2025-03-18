import MainPage from './components/Main'
import {Route,Routes, useNavigate} from 'react-router-dom'
import './index.css'
import Registration from './components/Registeration'
import RegistrationError from './components/RegisterationError'
import OtherError from './components/OtherError'
import NotFound404 from './components/NotFoundError'
import Login from './components/login'
import { AuthProvider, useAuth } from './AuthContext';
import FrameworkSelector from './components/ModelSelection';
import Circuit from './components/Circuit';
import PricingSection from './components/pricing';
import Dashboard from './components/Dashboard';
import Analytics from './components/Analytics'
import { ApplyCredits } from './components/Applyingcredits'


const ProtectedRoute = ({ children }) => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) {
    return navigate("/login");
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
      <Route path='/login' element={<Login />}/>
      <Route path='/dashboard' element={<Dashboard/>}/>
      <Route path="*" element={<Login/>}/> {/*The Landing page is to be redirected*/}
      <Route path="/pricing" element={<PricingSection/>}/>
      <Route path='/selection' element={<FrameworkSelector/>}/>
      <Route path='/dashboard' element={<Dashboard/>}/>
      <Route path='/analytics' element={<Analytics/>}/>
      <Route path="/applycredits" element={<ApplyCredits/>}/>
      <Route path="/circuit" element={<Circuit/>}/>{/*The Circuit is formed but for trail version*/}
     </Routes>
     </AuthProvider>
  )
}

export default App
