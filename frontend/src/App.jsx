import { useState } from 'react'
import './App.css'
import QuizForm from './components/QuizForm'
import Results from './components/Results'
import logo from './assets/logo.svg'


function App() {
  const [matches, setMatches] = useState(null)
  const [adopterProfile, setAdopterProfile] = useState(null)

  const handleMatchesReceived = (matches, profile) => {
    setMatches(matches)
    setAdopterProfile(profile)
  }

  const handleRetakeQuiz = () => {
    setMatches(null)
    setAdopterProfile(null)
  }

  return (
    <div>
      <h1>
        <img src={logo} alt="PawPair logo" className="logo" />
        PawPair
      </h1>
      {matches ? (
        <Results matches={matches} adopterProfile={adopterProfile} onRetakeQuiz={handleRetakeQuiz} />
      ) : (
        <QuizForm onMatchesReceived={handleMatchesReceived} />
      )}
    </div>
  )
}

export default App
