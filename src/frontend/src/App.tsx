import { useState } from 'react'
import Body from './Body'
import Footer from './Footer'
import Header from './Header'
import Music from './Music'
import AIFriend from './AIFriend'
import { AnimatePresence, motion } from 'motion/react'
import { QueryAudio, QueryImage, UpdateDataset } from './api'

function App() {
  const [currentMusic, setCurrentMusic] = useState<Music | undefined>(undefined)
  const [query, setCurrentQuery] = useState<string>("")
  const [aiState, setAIState] = useState<"dormant" | "awake">("dormant")
  const [appState, setAppState] = useState<"default" | "mainoptions" | "dataset" | "query" | "image" | "audio" | "searchresults">("default")
  const [timeTaken, setTimeTaken] = useState<number>(0)

  const aiTrigger = () => {
    setAIState("awake")
    setAppState("mainoptions")
    setCurrentQuery("")
    setCurrentMusic(undefined)
  }

  const datasetTrigger = () => {
    setAppState("dataset")
  }

  const queryTrigger = () => {
    setAppState("query")
  }

  const imageQueryTrigger = () => {
    setAppState("image")
  }

  const audioQueryTrigger = () => {
    setAppState("audio")
  }

  const cancelAI = () => {
    setAIState("dormant")
    setAppState("default")
  }

  const showResults = () => {
    setAIState("dormant")
    setAppState("searchresults")
    setCurrentQuery("")
    setCurrentMusic(undefined)
  }

  const onDatasetSelected = async (files: FileList) => {
    await UpdateDataset(files[0])
    cancelAI()
  }

  const onImageSelected = async (files: FileList) => {
    const startTime = Date.now()
    await QueryImage(files[0])
    setTimeTaken((Date.now() - startTime) / 1000)
    showResults()
  }

  const onAudioSelected = async (files: FileList) => {
    const startTime = Date.now()
    await QueryAudio(files[0])
    setTimeTaken((Date.now() - startTime) / 1000)
    showResults()
  }

  return (
    <AnimatePresence>
      <AIFriend state={aiState} />
      {
        (
          appState === "audio" &&
            <div className="block h-screen w-screen bg-[#12801b]">
              <motion.div className="flex flex-col gap-4 items-center bg-[#034774] h-screen w-screen"
                initial={{opacity: 0}}
                animate={{opacity: 1}}
                exit={{opacity: 0}}
              >
                <div className="flex flex-row-reverse h-1/2 w-full p-4">
                  <button className="text-white h-fit" onClick={cancelAI}>
                    Back
                  </button>
                </div>
                <div className="text-white text-5xl text-center">
                  Thats good! Just let me know how it sounds like and I'll tell you which song it is.
                </div>
                <div className="flex-grow flex w-full gap-20 items-center justify-center">
                  <input type="file" id="datasetinput" className="hidden" accept=".mid, .midi" onChange={(e) => {onAudioSelected(e.target.files!)}}/>
                  <label htmlFor="datasetinput" className="w-52 h-24 text-center content-center text-white text-xl z-50 bg-gray-900 hover:bg-black rounded-2xl">
                    Upload Audio
                  </label>
                </div>
              </motion.div>
            </div>
        )
      }
      {
        (
          appState === "image" &&
            <div className="block h-screen w-screen bg-[#12801b]">
              <motion.div className="flex flex-col gap-4 items-center bg-[#a01616] h-screen w-screen"
                initial={{opacity: 0}}
                animate={{opacity: 1}}
                exit={{opacity: 0}}
              >
                <div className="flex flex-row-reverse h-1/2 w-full p-4">
                  <button className="text-white h-fit" onClick={cancelAI}>
                    Back
                  </button>
                </div>
                <div className="text-white text-5xl text-center">
                  I can work with that! Just give me a picture of it and I'll see which song it matches with.
                </div>
                <div className="flex-grow flex w-full gap-20 items-center justify-center">
                  <input type="file" id="datasetinput" className="hidden" accept="image/*" onChange={(e) => {onImageSelected(e.target.files!)}}/>
                  <label htmlFor="datasetinput" className="w-52 h-24 text-center content-center text-white text-xl z-50 bg-gray-900 hover:bg-black rounded-2xl">
                    Upload Image
                  </label>
                </div>
              </motion.div>
            </div>
        )
      }
      {
        (
          appState === "query" &&
            <div className="block h-screen w-screen bg-[#6c1083]">
              <motion.div className="flex flex-col gap-4 items-center bg-[#12801b] h-screen w-screen"
                initial={{opacity: 0}}
                animate={{opacity: 1}}
                exit={{opacity: 0}}
              >
                <div className="flex flex-row-reverse h-1/2 w-full p-4">
                  <button className="text-white h-fit" onClick={cancelAI}>
                    Back
                  </button>
                </div>
                <div className="text-white text-5xl text-center">
                  Let me help with that. Tell me what you remember about the song you're thinking of.
                </div>
                <div className="flex-grow flex w-full gap-20 items-center justify-center">
                  <button className="w-52 h-36 text-white z-50" onClick={imageQueryTrigger}>
                    I remember its album cover
                  </button>
                  <button className="w-52 h-36 text-white z-50" onClick={audioQueryTrigger}>
                    I remember a part of it
                  </button>
                </div>
              </motion.div>
            </div>
        )
      }
      {
        (
          appState === "dataset" &&
            <div className="block h-screen w-screen bg-[#6c1083]">
              <motion.div className="flex flex-col gap-4 items-center bg-[#be9818] h-screen w-screen"
                initial={{opacity: 0}}
                animate={{opacity: 1}}
                exit={{opacity: 0}}
              >
                <div className="flex flex-row-reverse h-1/2 w-full p-4">
                  <button className="text-white h-fit" onClick={cancelAI}>
                    Back
                  </button>
                </div>
                <div className="text-white text-5xl text-center">
                  Sure thing! Just upload the new dataset here.
                </div>
                <div className="flex-grow flex w-full gap-20 items-center justify-center">
                  <input type="file" id="datasetinput" className="hidden" accept=".zip" onChange={(e) => {onDatasetSelected(e.target.files!)}}/>
                  <label htmlFor="datasetinput" className="w-52 h-24 text-center content-center text-white text-xl z-50 bg-gray-900 hover:bg-black rounded-2xl">
                    Upload Dataset
                  </label>
                </div>
              </motion.div>
            </div>
        )
      }
      {
        (
          appState === "mainoptions" &&
            <div className="block h-screen w-screen bg-[#0d0c1d]">
              <motion.div className="flex flex-col gap-4 items-center bg-[#6c1083] h-screen w-screen"
                initial={{opacity: 0}}
                animate={{opacity: 1}}
                exit={{opacity: 0}}
              >
                <div className="flex flex-row-reverse h-1/2 w-full p-4">
                  <button className="text-white h-fit" onClick={cancelAI}>
                    Back
                  </button>
                </div>
                <div className="text-white text-5xl text-center">
                  How can I help you?
                </div>
                <div className="flex-grow flex w-full gap-20 items-center justify-center">
                  <button className="w-52 h-36 text-white z-50" onClick={datasetTrigger}>
                    I want to change the dataset
                  </button>
                  <button className="w-52 h-36 text-white z-50" onClick={queryTrigger}>
                    I'm having trouble remembering a song I've heard                    
                  </button>
                </div>
              </motion.div>
            </div>
        )
      }
      {
        (
          (appState === "default" || appState === "searchresults") &&
            <motion.div className="flex flex-col bg-[#0d0c1d] h-screen w-screen"
              initial={false}
              animate={{opacity: 1}}
              exit={{opacity: 0}}
            >
              <button className="fixed bottom-2 right-8 w-20 h-20 outline-none bg-transparent z-50" onClick={aiTrigger} />
              <Header searchCallback={setCurrentQuery} result={appState === "searchresults"} timeTaken={timeTaken}/>
              <Body result={appState === "searchresults"} query={query} musicCallback={setCurrentMusic} className="flex-grow bg-[#161b33] p-2 mx-2 rounded-xl max-h-full" />
              <Footer music={currentMusic} />
            </motion.div>
        )
      }
    </AnimatePresence>
  )
}

export default App
