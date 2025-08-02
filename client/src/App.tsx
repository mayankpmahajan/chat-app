import './App.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import Login from './components/Login'
import Signup from './components/Signup'
import ResetPassword from './components/ResetPassword'


function App() {


  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login/>}></Route>
        <Route path="/signup" element={<Signup/>}></Route>
        <Route path="/reset-password/:uid/:token" element={<ResetPassword/>}></Route>

      </Routes>
    </Router>
  )
}

export default App
