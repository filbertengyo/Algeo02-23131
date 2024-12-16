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

export async function GetMusic(offset: number) {
    return testdata[offset]
}

export async function GetMusicList(query: string, offset: number, count: number) {
    return testdata.filter((music) => music.name.startsWith(query)).slice(offset, offset + count)
}

export async function GetMusicCount(query: string) {
    return testdata.filter((music) => music.name.startsWith(query)).length
}

export async function GetQueryResult(offset: number, count: number) {

}

export async function GetQueryCount() {

}

export async function UpdateDataset(file: File) {

}

export async function QueryImage(file: File) {
    return 1
}

export async function QueryAudio(file: File) {
    return 0
}