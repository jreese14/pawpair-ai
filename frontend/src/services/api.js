const API_BASE_URL = 'http://localhost:8000'

export async function getHealth() {
  const response = await fetch(`${API_BASE_URL}/health`)
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`)
  }
  return response.json()
}

export async function getPets() {
  const response = await fetch(`${API_BASE_URL}/pets`)
  if (!response.ok) {
    throw new Error(`Fetching pets failed: ${response.status}`)
  }
  return response.json()
}
