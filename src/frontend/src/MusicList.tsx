import Music from "./Music";
import MusicCard from "./MusicCard";

interface MusicListProps {
    musicList?: Music[]
    musicCallback?: (music: Music) => void
    className?: string
    ref?: React.Ref<HTMLDivElement>
}

export default function MusicList({ musicList, musicCallback, className, ref }: MusicListProps) {
    return(
        <div className={className} ref={ref}>
            {
                musicList?.map(music => <MusicCard music={music} musicCallback={musicCallback} key={music.name}/>)
            }
        </div>
    )
}