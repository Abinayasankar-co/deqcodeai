import MainPage from './components/Main'
import {Route,Routes} from 'react-router-dom'
import './index.css'

function App() {
  return (
    <>
     <Routes>
      <Route path="/design" element={<MainPage />} />
     </Routes>
    </>
  )
}

export default App
