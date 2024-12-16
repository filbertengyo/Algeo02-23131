import Music from "./Music";
import MusicList from "./MusicList";


interface BodyProps {
    query?: string
    musicCallback?: (music: Music) => void
    className?: string
}

export default function Body({ query, musicCallback, className }: BodyProps) {

    return (
        <div className={className}>
            <div className="flex w-full h-full gap-2">
                <div className="h-full content-center">
                    <button>
                        Prev
                    </button>
                </div>
                <MusicList className="flex-grow flex justify-center items-center h-full" />
                <div className="h-full content-center">
                    <button>
                        Next
                    </button>
                </div>
            </div>
        </div>
    )
}