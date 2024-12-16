import numpy as np
from audio_preprocessor import AudioPreprocessor as prep

class AudioProcessor:
    def __init__(self):
        self.window_size = 20
        self.slide = 4

    @staticmethod
    def pitch_normalization(notes):
        notes_mean = np.mean(notes)
        notes_standard_dev = np.std(notes)
        normalized_note = []

        if notes_standard_dev == 0:
            return np.zeros_like(notes)
        for note in notes:
            normalized_note.append((note - notes_mean) / notes_standard_dev)
        
        return normalized_note
    @staticmethod
    def getNotes(midi_messages):
        notes = []
        for message in midi_messages:
            notes.append(message['note'])
        return notes

    def create_histogram(self, notes, bin_range=(1, 128)):
        bin_size = 1
        min_bin, max_bin = bin_range
        bin_count = int((max_bin - min_bin) / bin_size)
        histogram = np.zeros(bin_count)
        
        for note in notes:
            bin_index = int((note - min_bin) // bin_size)  
            if 0 <= bin_index < bin_count:
                histogram[bin_index] += 1
        if np.sum(histogram) == 0:
            return histogram
        
        return histogram / np.sum(histogram)  

    def absolute_tone_based(self, notes):
        return self.create_histogram(notes, bin_range=(1, 128))  

    def relative_tone_based(self, notes):
        diffs = [notes[i] - notes[i-1] for i in range(1, len(notes))]
        return self.create_histogram(diffs, bin_range=(-128, 128))

    def first_tone_based(self, notes):
        first_note = notes[0] if len(notes) > 0 else 0
        diffs = [note - first_note for note in notes]
        return self.create_histogram(diffs, bin_range=(-128, 128))

    @staticmethod
    def calculate_similarity(vec1, vec2):
        if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
            return 0
        return np.dot(vec1,vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def windowing(self, notes):
        windows = []
        start = 0
        while start + self.window_size <= len(notes):
            window = notes[start:start + self.window_size]
            windows.append(window)
            start += self.slide  # Sliding window
        return windows


    def main_process(self, input_file_path, audiodb_folder_path, map_folder_path):
        audio_list = prep.load_mapper(map_folder_path)

        input_normalized = self.pitch_normalization(self.getNotes(prep.extract_midi(input_file_path)))
        input_windows = self.windowing(input_normalized)

        input_atb = []
        input_rtb = []
        input_ftb = []

        for window in input_windows:
            input_atb.append(self.absolute_tone_based(window))
            input_rtb.append(self.relative_tone_based(window))
            input_ftb.append(self.first_tone_based(window))

        similarities = {}

        # Proses untuk setiap audio dalam database
        for audio in audio_list:
            audiodb_file_path = prep.load_audiodb(audiodb_folder_path, audio)
            
            audio_normalized = self.pitch_normalization(self.getNotes(prep.extract_midi(audiodb_file_path)))
            audio_windows = self.windowing(audio_normalized)

            audio_atb = []
            audio_rtb = []
            audio_ftb = []

            for window in audio_windows:
                audio_atb.append(self.absolute_tone_based(window))
                audio_rtb.append(self.relative_tone_based(window))
                audio_ftb.append(self.first_tone_based(window))

            best_similarity = -1  # Mulai dengan nilai similarity yang sangat rendah

            # Lakukan perhitungan similarity untuk setiap window
            for audio_win_atb, audio_win_rtb, audio_win_ftb in zip(audio_atb, audio_rtb, audio_ftb):
                for input_win_atb, input_win_rtb, input_win_ftb in zip(input_atb, input_rtb, input_ftb):
                    similarity_atb = self.calculate_similarity(input_win_atb, audio_win_atb)
                    similarity_rtb = self.calculate_similarity(input_win_rtb, audio_win_rtb)
                    similarity_ftb = self.calculate_similarity(input_win_ftb, audio_win_ftb)

                    # Ambil nilai maksimum dari tiga similarity fitur
                    similarity_value = (0.5 * similarity_atb) + (0.3 * similarity_rtb) + (0.2 * similarity_ftb)
                    best_similarity = max(best_similarity, similarity_value)

            # Simpan hasil similarity terbaik untuk audio
            similarities[audio] = best_similarity

        # Urutkan hasil similarity berdasarkan nilai tertinggi
        sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        return sorted_similarities

    @staticmethod
    def display_query_results(results):
        for result in results:
            print(f"Song File: {result[0]} , Similarity: {result[1]}")

# my personal test
# audio_processor = AudioProcessor()
# input_file_path = './audio_1.midi'
# audiodb_folder_path = './audio_db'
# map_folder_path = './mapper'

# query_results = audio_processor.main_process(input_file_path, audiodb_folder_path, map_folder_path)
# audio_processor.display_query_results(query_results)
