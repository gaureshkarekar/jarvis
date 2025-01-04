import { useEffect } from 'react'
import IronManGif from './components/IronManGif'
import JarvisGif from './components/JarvisGif'

import './App.css'


function App() {

  useEffect( ()=>{
    fetch("http://127.0.0.1:5000/jarvis");
  },[]);

  return (
    <>
      <JarvisGif />
      <IronManGif />
    </>
  )
}

export default App
