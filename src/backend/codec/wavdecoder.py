import struct
from musicdata import Note, MusicData

def DecodeWaveFile(filepath : str) -> MusicData:
    with open(filepath, "rb") as file:
        return DecodeWave(file.read())

def DecodeWave(data : bytes) -> MusicData:
    if len(data) < 36: return

    riffChunckId, riffChunckSize = struct.unpack("4sI", data[:8])
    if riffChunckId != b"RIFF" or len(data) - 8 < riffChunckSize: return

    waveFormatId, = struct.unpack("4s", data[8:12])
    if waveFormatId != b"WAVE": return

    fmtChunckId, fmtChunckSize, fmtAudioFormat, fmtNumChannels, fmtSampleRate, fmtByteRate, fmtBlockAlign, fmtBitsPerSample = struct.unpack("4sIHHIIHH", data[12:36])
    if fmtChunckId != b"fmt ": return
    if fmtAudioFormat != 1 or fmtChunckSize != 16: return
    if fmtBlockAlign != fmtNumChannels * fmtBitsPerSample // 8: return
    if fmtByteRate != fmtBlockAlign * fmtSampleRate: return

    dataChunckId, dataChuckSize = struct.unpack("4sI", data[36:44])
    if dataChunckId != b"data": return

    rawAudioData = []

    for i in range(dataChuckSize // fmtBlockAlign):
        sum = 0

        for j in range(fmtNumChannels):
            bytesPerSample = fmtBitsPerSample // 8
            startByte = 44 + i * fmtBlockAlign + j * bytesPerSample
            sum += int.from_bytes(data[startByte:(startByte + bytesPerSample)], byteorder="little", signed=True)
        
        avg = sum / fmtNumChannels

        if fmtBitsPerSample <= 8 and avg < 0:
            avg += 128
        else:
            avg -= 128

        rawAudioData.append(avg)
