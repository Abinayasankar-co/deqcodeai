import MainPage from './components/Main'
import {Route,Routes} from 'react-router-dom'

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
