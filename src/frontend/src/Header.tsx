import SearchBar from "./SearchBar"


interface HeaderProps {
    searchCallback?: (query: string) => void
    result?: boolean
    timeTaken?: number
}

export default function Header({ searchCallback, result, timeTaken }: HeaderProps) {
    return (
        <div className="flex flex-col items-center bg-[#0d0c1d] w-full gap-4 p-4 pb-6">
            <div className="text-5xl w-fit text-white">
                EDP445
            </div>
            {
                !result &&
                <SearchBar
                    className="w-[48rem] max-w-full h-4"
                    searchCallback={searchCallback}
                />
            }
            {
                result &&
                (
                    <div className="text-xl w-fit text-white">
                        {`Searching took ${timeTaken} seconds`}
                    </div>
                )
            }
        </div>
    )
}