interface SearchBarProps {
    searchCallback?: ((query: string) => void)
    className?: string
}

export default function SearchBar({ searchCallback, className }: SearchBarProps) {
    const handleSubmit = (data: FormData) => {
        const query = data.get("query") as string
        if (searchCallback) searchCallback(query)
    }
    
    return (
        <div className={className}>
            <form action={handleSubmit}>
                <div className="flex bg-white rounded-md w-full items-center px-2 py-0 gap-2">
                    <input name="query"  className="flex-grow h-full bg-transparent outline-none"/>
                    <button type="submit" className="h-full bg-transparent p-0 text-black hover:text-gray-700 transition-colors border-none">
                        Search
                    </button>
                </div>
            </form>
        </div>
    )
}