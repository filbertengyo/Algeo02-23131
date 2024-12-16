

interface AIFriendProps {
    state: "dormant"
}

export default function AIFriend({ state }: AIFriendProps) {
    if (state === "dormant") {
        return (
            <div className="fixed bottom-2 right-2 w-20 h-20 bg-black">
                
            </div>
        )
    }
}