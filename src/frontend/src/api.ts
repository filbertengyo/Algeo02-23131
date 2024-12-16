'use server'

import Music from "./Music"

const testdata: Music[] = new Array(64)
let i: number
for (i = 0; i < testdata.length; i++) {
    testdata[i] = {
        audiosrc: `audio${i}.mid`,
        coversrc: `cover${i}.png`,
        name: `test music ${i}`
    }
}

export function GetMusic(offset: number): Music {
    return testdata[offset]
}

export function GetMusicList(query: string, offset: number, count: number) {
    return testdata.filter((music) => music.name.startsWith(query)).slice(offset, offset + count)
}

export function GetMusicCount(query: string) {
    return testdata.filter((music) => music.name.startsWith(query)).length
}