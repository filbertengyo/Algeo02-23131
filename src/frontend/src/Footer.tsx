import Music from "./Music";
import MusicControls from "./MusicControls";
import MusicInfo from "./MusicInfo";

interface FooterProps {
    music?: Music
}

export default function Footer({ music }: FooterProps) {
    return (
        <div className="flex justify-center w-full h-24 p-2 gap-2 bg-[#0d0c1d]">
            <MusicInfo className="flex-grow basis-1 flex gap-2 items-center h-full min-w-20" source={music} />
            <MusicControls className="flex-grow h-full max-w-[48rem] min-w-16" source={music} />
            <div className="flex-grow basis-1 h-full min-w-20" />
        </div>
    )
}