import { useRef } from "react"

interface SearchBarProps {
    searchCallback?: ((query: string) => void)
    className?: string
}

export default function SearchBar({ searchCallback, className }: SearchBarProps) {
    const inputFieldRef = useRef<HTMLInputElement>(null)

    const handleSubmit = () => {
        if (searchCallback) searchCallback(inputFieldRef.current?.value || "")
    }
    
    return (
        <div className={className}>
            <div className="flex bg-white rounded-md w-full items-center px-2 py-0 gap-2">
                <input ref={inputFieldRef} onKeyDown={(e) => {if (e.key === "Enter") handleSubmit()}} className="flex-grow h-full bg-transparent outline-none"/>
                <button onClick={handleSubmit} className="h-full bg-transparent p-0 text-black hover:text-gray-700 transition-colors border-none">
                    Search
                </button>
            </div>
        </div>
    )
}