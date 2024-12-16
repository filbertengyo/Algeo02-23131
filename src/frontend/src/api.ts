'use server'

import axios from "axios"

export async function GetMusic(offset: number) {
    return (await axios.get(`${import.meta.env.VITE_API_SERVER}/api/getmusic/${offset}`)).data
}

export async function GetMusicList(query: string, offset: number, count: number) {
    return (await axios.get(`${import.meta.env.VITE_API_SERVER}/api/getmusiclist/_${query}/${offset}/${count}`)).data
}

export async function GetMusicCount(query: string) {
    return (await axios.get(`${import.meta.env.VITE_API_SERVER}/api/getmusiccount/_${query}`)).data['count']
}

export async function GetQueryResult(offset: number, count: number) {
    return (await axios.get(`${import.meta.env.VITE_API_SERVER}/api/getqueryresult/${offset}/${count}`)).data
}

export async function UpdateDataset(file: File) {
    const formData = new FormData()
    formData.append('dataset', file)
    await axios.post(`${import.meta.env.VITE_API_SERVER}/api/updatedataset`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
    })
}

export async function QueryImage(file: File) {
    const formData = new FormData()
    formData.append('filename', file.name)
    formData.append('query', file)
    await axios.post(`${import.meta.env.VITE_API_SERVER}/api/queryimage`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
    })
}

export async function QueryAudio(file: File) {
    const formData = new FormData()
    formData.append('filename', file.name)
    formData.append('query', file)
    await axios.post(`${import.meta.env.VITE_API_SERVER}/api/queryaudio`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
    })
}