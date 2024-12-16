import { useEffect, useRef, useState } from "react";
import Music from "./Music";
import MusicList from "./MusicList";
import { GetMusicCount, GetMusicList, GetQueryResult } from "./api";


interface BodyProps {
    query?: string
    musicCallback?: (music: Music) => void
    className?: string
    result?: boolean
}

export default function Body({ query, musicCallback, className, result }: BodyProps) {
    const [pageSize, setPageSize] = useState(0)
    const [pageOffset, setPageOffset] = useState(0)
    const [musicList, setMusicList] = useState<Music[]>([])
    const musicListRef = useRef<HTMLDivElement | null>(null)
    const musicCountRef = useRef<number>(0)

    useEffect(() => {
        const onResize = () => {
            if (!musicListRef.current) return

            const width = musicListRef.current.offsetWidth
            const height = musicListRef.current.offsetHeight

            const cardWidth = 12 * parseFloat(getComputedStyle(document.documentElement).fontSize)
            const cardHeight = 16 * parseFloat(getComputedStyle(document.documentElement).fontSize)

            const colCount = Math.floor(width / cardWidth)
            const rowCount = Math.floor(height / cardHeight)
            
            const newPageSize = colCount * rowCount
            const newPageOffset = pageOffset / newPageSize

            setPageSize(newPageSize)
            setPageOffset(newPageOffset)
        }

        window.addEventListener('resize', onResize)

        onResize()

        return () => {
            window.removeEventListener('resize', onResize)
        }
    }, [])

    useEffect(() => {
        setPageOffset(0)
        if (pageOffset === 0) {
            if (result) {
                GetQueryResult(0, pageSize).then((res) => {setMusicList(res)})
                GetMusicCount().then((res) => {musicCountRef.current = res})
            } else {
                GetMusicList(query || "", 0, pageSize).then((res) => {setMusicList(res)})
                GetMusicCount(query || "").then((res) => {musicCountRef.current = res})
            }
        }
    }, [query])

    useEffect(() => {
        if (result) {
            GetQueryResult(0, pageSize).then((res) => {setMusicList(res)})
            GetMusicCount().then((res) => {musicCountRef.current = res})
        } else {
            GetMusicList(query || "", 0, pageSize).then((res) => {setMusicList(res)})
            GetMusicCount(query || "").then((res) => {musicCountRef.current = res})
        }
    }, [pageSize, pageOffset])

    return (
        <div className={className}>
            <div className="flex w-full h-full gap-2">
                <div className="flex flex-col h-full w-20 min-w-20 content-center justify-center">
                    <button
                        className="text-white"
                        onClick={() => {setPageOffset(Math.max(pageOffset - pageSize, 0))}}
                        disabled={pageOffset <= 0}
                    >
                        Prev
                    </button>
                </div>
                <MusicList musicList={musicList} musicCallback={musicCallback} className="flex-grow flex flex-wrap justify-center items-center h-full" ref={musicListRef}/>
                <div className="flex flex-col h-full w-20 min-w-20 content-center justify-center">
                    <button
                        className="text-white"
                        onClick={() => {setPageOffset(pageOffset + pageSize)}}
                        disabled={pageOffset + pageSize >= musicCountRef.current}
                    >
                        Next
                    </button>
                </div>
            </div>
        </div>
    )
}