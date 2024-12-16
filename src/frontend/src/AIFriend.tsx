import Lottie from '@lottielab/lottie-player/react'
import { motion } from "motion/react"

interface AIFriendProps {
    state: "dormant" | "awake"
}

const aiVariants = {
    dormant: { bottom: "-80.8rem", right: "-80.8rem", height: "88rem", width: "88rem" },
    awake: { transform: "translate(-7.8rem, -24rem)", top: "50%", left: "50%", height: "256rem", width: "256rem" }
}

const aiAnimations = {
    "dormant": "https://cdn.lottielab.com/l/5TaCPnbviEhcuZ.json",
    "awake": "https://cdn.lottielab.com/l/EhCohuGV7YbsPD.json"
}

export default function AIFriend({ state }: AIFriendProps) {
    return (
        <motion.div className="fixed z-40"
            variants={aiVariants}
            initial={false}
            animate={state}
        >
            <Lottie src={aiAnimations[state]} className="absolute h-fill w-fill" autoplay />
        </motion.div>
    )
}