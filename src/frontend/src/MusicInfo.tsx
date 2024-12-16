import Music from "./Music"

interface MusicProps {
    source?: Music
    className?: string
}

export default function MusicInfo({source, className}: MusicProps) {
    return (
        <div className={className}>
            <div className="h-full max-w-[25%] aspect-square content-center">
                {source && <img className="w-full aspect-square object-cover bg-black" src={source.coversrc}/>}
                {!source && <img className="w-full aspect-square bg-black"/>}
            </div>
            <div className="text-xl text-white content-center text-left">
                {source? source.name : "..."}
            </div>
        </div>
    )
}