import MainPage from './components/Main'
import {Route,Routes} from 'react-router-dom'
import './index.css'
import Registration from './components/Registeration'
import RegistrationError from './components/RegisterationError'
import OtherError from './components/OtherError'
import NotFound404 from './components/NotFoundError'

function App() {
  return (
    <>
     <Routes>
      <Route path="/design" element={<MainPage />} />
      <Route path='/register' element={<Registration/>}/>
      <Route path='/registerion_error' element={<RegistrationError/>}/>
      <Route path='/error' element={<OtherError/>}/>
      <Route path='/canthandle' element={<NotFound404/>}/>
     </Routes>
    </>
  )
}

export default App
