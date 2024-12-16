import os
import json
import numpy as np
import time
from PIL import Image
from image_preprocessor import ImagePreprocessor

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

        all_data = []
        self.generateRawImageDataFiles()
        self.generateDataAverageFile()
        self.generateNormalizedDataFiles()

        for filename in [item['pic_name'] for item in self.mapper]:
            normalized_data = self.getNormalizedData(filename)
            all_data.append(normalized_data)

        X = np.array(all_data)
        self.mean_vector = np.mean(X, axis=0)
        X_centered = X - self.mean_vector

        U, S, VK = np.linalg.svd(X_centered, full_matrices=False)
        self.U_k = VK[:self.k].T  
        self.Z = np.dot(X_centered, self.U_k)  

    def search(self, filepath: str):
        '''Search for the most similar images to the given file and return the duration.'''
        query_name = os.path.basename(filepath)
        self.generateRawImageDataFile(filepath)
        self.generateNormalizedDataFile(query_name)
        query_data = self.getNormalizedData(query_name)

        query_projection = np.dot(query_data - self.mean_vector, self.U_k)

        distances = []
        for i, filename in enumerate([item['pic_name'] for item in self.mapper]):
            distance = np.linalg.norm(query_projection - self.Z[i])
            distances.append((filename, distance))

        distances.sort(key=lambda x: x[1])

        for filename, distance in distances:
            print(f"{filename}: Jarak = {distance:.4f}")

        return distances
