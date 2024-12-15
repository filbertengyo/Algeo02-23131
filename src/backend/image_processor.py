import os
import json
import numpy as np
from PIL import Image
from backend.image_preprocessor import ImagePreprocessor

class ImageProcessor(ImagePreprocessor):
    '''Performs PCA with SVD and similarity calculation for images.'''

    def __init__(self, dimension: tuple[int, int], dir: str, k: int):
        '''Initialize with dimension, directory, and number of principal components (k).'''
        super().__init__(dimension, dir)
        self.k = k  
        self.mean_vector = None
        self.U_k = None  
        self.Z = None  
        self.mapper = {}  

    def load(self, folderpath: str):
        '''Load mapper.json and prepare data matrix Z.'''
        mapper_path = os.path.join(folderpath, 'mapper.json')
        with open(mapper_path, 'r') as file:
            self.mapper = json.load(file)

        print("Mapper loaded. Processing images...")
        all_data = []
        self.generateRawImageDataFiles()
        self.generateDataAverageFile()
        self.generateNormalizedDataFiles()

        for filename, _ in self.mapper.items():
            normalized_data = self.getNormalizedData(filename.removesuffix('.png'))
            all_data.append(normalized_data)

        X = np.array(all_data)
        self.mean_vector = np.mean(X, axis=0)
        X_centered = X - self.mean_vector

        U, S, VK = np.linalg.svd(X_centered, full_matrices=False)
        self.U_k = VK[:self.k].T  
        self.Z = np.dot(X_centered, self.U_k)  

        print("Data loaded and projected into PCA space.")

    def search(self, filepath: str):
        '''Search for the most similar images to the given file.'''
        query_name = os.path.basename(filepath).removesuffix('.png')
        self.generateRawImageDataFile(filepath)
        self.generateNormalizedDataFile(query_name)
        query_data = self.getNormalizedData(query_name)

        query_projection = np.dot(query_data - self.mean_vector, self.U_k)

        distances = []
        for i, (filename, _) in enumerate(self.mapper.items()):
            distance = np.linalg.norm(query_projection - self.Z[i])
            distances.append((filename, distance))

        distances.sort(key=lambda x: x[1])

        print("Hasil pencarian terdekat:")
        for filename, distance in distances[:5]:
            print(f"{filename}: Jarak = {distance:.4f}")
        return distances[:5]
