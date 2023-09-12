import React from 'react'
const BACKEND_PROXY = "http://localhost:8080";

function App() {
  return (
    <>
    <div><button onClick={() => window.location.href = `${BACKEND_PROXY}/login`}> login to spotify</button></div>
    <div><button onClick={() => fetch(`${BACKEND_PROXY}/shuffle`).then(res => res.json()).then(res => console.log(res))}>
       shuffle (after log in)</button></div>
    </>
  )
}

export default App