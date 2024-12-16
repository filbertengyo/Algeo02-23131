import Body from './Body'
import Footer from './Footer'
import Header from './Header'

function App() {
  return (
    <div className="flex flex-col bg-[#0d0c1d] h-screen w-screen">
      <Header/>
      <Body className="flex-grow bg-[#161b33] p-2 mx-2 rounded-xl max-h-full" />
      <Footer/>
    </div>
  )
}

export default App
