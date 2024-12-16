import { forwardRef } from "react";
import Music from "./Music";
import MusicCard from "./MusicCard";

interface MusicListProps {
    musicList?: Music[]
    musicCallback?: (music: Music) => void
    className?: string
}

const MusicList = forwardRef<HTMLDivElement, MusicListProps>(({ musicList, musicCallback, className }: MusicListProps, ref?) => {
    return (
        <div className={className} ref={ref}>
            {
                musicList?.map(music => <MusicCard music={music} musicCallback={musicCallback} key={music.name}/>)
            }
        </div>
    )
})

export default MusicList