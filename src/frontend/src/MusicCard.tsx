import Music from "./Music";


interface MusicCardProps {
    music: Music
    musicCallback?: (music: Music) => void
}

export default function MusicCard({ music, musicCallback }: MusicCardProps) {
    return (
        <div className="rounded-xl w-48 h-fit p-2 hover:bg-[#0d0c1d] transition-colors flex flex-col items-center justify-center">
            <img className="w-full aspect-square object-cover rounded-xl bg-black" src={music.coversrc} />
            <div className="flex flex-row gap-2 w-full p-2">
                <div className="flex-grow text-base text-white">
                    {music.name}
                </div>
                <button className="p-0 px-2 text-sm rounded-xl text-white" onClick={() => { if (musicCallback) musicCallback(music) }} disabled={musicCallback === undefined}>
                    Play
                </button>
            </div>
        </div>
    )
}