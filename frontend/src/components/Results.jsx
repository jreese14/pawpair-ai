function Results({ matches }) {
  return (
    <div>
      <h1>Your Matches</h1>
      <p>Found {matches.length} matches</p>
      {matches.map((match, index) => (
        <pre key={index}>{JSON.stringify(match, null, 2)}</pre>
      ))}
    </div>
  )
}

export default Results
