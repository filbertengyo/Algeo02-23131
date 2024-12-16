import Music from "./Music";
import MusicCard from "./MusicCard";

interface MusicListProps {
    musicList?: Music[]
    className?: string
}

export default function MusicList({ musicList, className }: MusicListProps) {
    return(
        <div className={className}>
            <MusicCard music={{ audiosrc: "", coversrc: "", name: "test" }}/>
        </div>
    )
}