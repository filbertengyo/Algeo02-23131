import os
import mido
import json

class AudioPreprocessor:
    # Fungsi untuk mengubah MIDI menjadi data berupa 'note' dan 'time'
    def extract_midi(midi_file_path):
        midi_file = mido.MidiFile(midi_file_path)
        channel_1_data = []

        for track in midi_file.tracks:
            for msg in track:
                if msg.type in ['note_on', 'note_off'] and msg.channel == 0:
                    channel_1_data.append({
                        'note': msg.note,
                        'time': msg.time
                    })
        return channel_1_data
    
    # Fungsi untuk memuat mapper.json
    def load_mapper(map_folder_path):
        map_file_path = os.path.join(map_folder_path, "mapper.json")
        with open(map_file_path, 'r') as f:
            map_list = json.load(f)
            audio_list = [item['audio_file'] for item in map_list]
        return audio_list
    
    def load_audiodb(audiodb_folder_path, audiodb_file_name):
        return os.path.join(audiodb_folder_path, audiodb_file_name)
