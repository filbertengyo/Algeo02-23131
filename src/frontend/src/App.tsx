import { useState } from 'react'
import Body from './Body'
import Footer from './Footer'
import Header from './Header'
import Music from './Music'
import AIFriend from './AIFriend'

function App() {
  const [currentMusic, setCurrentMusic] = useState<Music | undefined>(undefined)
  const [query, setCurrentQuery] = useState<string>("")

  return (
    <>
      <AIFriend state='dormant' />
      <div className="flex flex-col bg-[#0d0c1d] h-screen w-screen">
        <Header searchCallback={setCurrentQuery} />
        <Body query={query} musicCallback={setCurrentMusic} className="flex-grow bg-[#161b33] p-2 mx-2 rounded-xl max-h-full" />
        <Footer music={currentMusic} />
      </div>
    </>
  )
}

export default App
