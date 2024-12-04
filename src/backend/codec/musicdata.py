import struct

class Note:
    def __init__(self):
        self.timestamp : float = 0 # in beats
        self.volume : float = 0
        self.pitch : int = 0 # should be 0 - 127 inclusive
    
    def serialize(self):
        return struct.pack("dfb", self.tick, self.volume, self.pitch)
    
    def deserialize(self, data : bytes):
        self.tick, self.pitch = struct.unpack("dfb", data)

class MusicData:
    def __init__(self):
        self.bpm : int = 120
        self.offset : float = 0.0
        self.length : float = 0.0
        self.stream : list[Note] = []

    def serialize(self):
        data = bytearray(struct.pack("Iff", self.bpm, self.offset, self.length))
        
        for note in self.stream:
            data.append(note.serialize())
        
        return data
    
    def deserialize(self, data : bytes):
        self.bpm, self.offset, self.length = struct.unpack("Iff", data[:struct.calcsize("Iff")])

        self.stream.clear()
        datastream = data[struct.calcsize("Iff"):]

        while len(datastream) > 0:
            notedata = datastream[:struct.calcsize("dfb")]
            self.stream.append(Note().deserialize(notedata))
            datastream = datastream[struct.calcsize("dfb"):]
        
