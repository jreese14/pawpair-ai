import { useEffect, useState } from 'react'
import { getHealth, getPets } from './services/api'
import './App.css'

function App() {
  const [status, setStatus] = useState('Checking backend connection...')
  const [pets, setPets] = useState([])
  const [petsError, setPetsError] = useState(null)

  useEffect(() => {
    getHealth()
      .then((data) => setStatus(data.message))
      .catch(() => setStatus('Could not reach the backend.'))

    getPets()
      .then((data) => setPets(data))
      .catch(() => setPetsError('Could not load pets.'))
  }, [])

  return (
    <div>
      <h1>PawPair</h1>
      <h2>Backend Health Check</h2>
      <p>{status}</p>

      <h2>GET /pets Check</h2>
      {petsError && <p>{petsError}</p>}
      {!petsError && <p>{pets.length} pets loaded</p>}
      <ul>
        {pets.map((pet) => (
          <li key={pet.id}>
            {pet.name} — {pet.breed}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App
