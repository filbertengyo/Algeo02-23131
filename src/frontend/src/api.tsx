'use server'

import Music from "./Music"

export function GetMusic(offset: number) {
    return new Music()
}

export function GetMusicList(query: string, offset: number, count: number) {
    return []
}

export function GetMusicCount(query: string) {
    return 0
}