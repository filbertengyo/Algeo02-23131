import { useEffect, useRef, useState } from "react"
import Music from "./Music"

interface MusicProps {
    source?: Music
    className?: string
}

export default function MusicControls({ source, className }: MusicProps) {
    const [currentTime, setCurrentTime] = useState(0)
    const [playing, setPlaying] = useState(false)
    const audioRef = useRef<HTMLAudioElement | null>(null)
    const durationRef = useRef(0)

    useEffect(() => {
        audioRef.current = new Audio(source?.audiosrc)
        audioRef.current.load()

        const updateTime = () => {
            if (audioRef.current) {
                setCurrentTime(audioRef.current.currentTime)
            } else {
                setCurrentTime(0)
            }
        }

        audioRef.current.addEventListener("timeupdate", updateTime)
        
        durationRef.current = audioRef.current.duration? audioRef.current.duration : 0

        return () => {
            audioRef.current?.pause()
            setPlaying(false)
            setCurrentTime(0)
            durationRef.current = 0
            audioRef.current = null
        }
    }, [source])

    const play = () => {
        audioRef.current?.play();
    };

    const pause = () => {
        audioRef.current?.pause();
    };

    const playPause = () => {
        if (playing) {
            pause()
        } else
        {
            play()
        }
    }

    const seek = (time: number) => {
        if (audioRef.current) {
            audioRef.current.currentTime = time
        }
    }

    const formatTimestamp = (time: number) => {
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60);
        return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    }

    return (
        <div className={className}>
            <div className="flex flex-col gap-2 flex-grow h-full justify-center items-center">
                <div className="flex gap-2 w-full justify-center items-center">
                    <button type="button" className="text-white p-2" onClick={playPause} disabled={audioRef.current?.src != undefined}>
                        {playing? "Pause" : "Play"}
                    </button>
                </div>
                <div className="flex gap-2 w-full justify-center items-center">
                    <div className="h-full w-16 text-base text-white content-center text-right">
                        {formatTimestamp(currentTime)}
                    </div>
                    <input className="flex-grow h-full"
                        type="range"
                        min="0"
                        max={durationRef.current.toString()}
                        value={currentTime.toString()}
                        onChange={(e) => {seek(parseFloat(e.target.value))}}
                    />
                    <div className="h-full w-16 text-base text-white content-center text-left">
                        {formatTimestamp(durationRef.current)}
                    </div>
                </div>
            </div>
        </div>
    )
}