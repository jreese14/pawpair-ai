import { useEffect, useState } from 'react'
import { getHealth } from './services/api'
import './App.css'

function App() {
  const [status, setStatus] = useState('Checking backend connection...')

  useEffect(() => {
    getHealth()
      .then((data) => setStatus(data.message))
      .catch(() => setStatus('Could not reach the backend.'))
  }, [])

  return (
    <div>
      <h1>PawPair</h1>
      <h2>Backend Health Check</h2>
      <p>{status}</p>
    </div>
  )
}

export default App
