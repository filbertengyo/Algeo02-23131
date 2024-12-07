import numpy as np
from image_preprocessor import ImagePreprocessor 

class ImageProcessor:
    def __init__(self, folderpath, target_dim=(64, 64)):
        self.directory = folderpath
        self.preprocessor = ImagePreprocessor(target_dim, folderpath)
        self.mean = None
        self.pca_components = None

    def PCAEigenVec(self, X, num_components=3):
        N = X.shape[0]
        self.mean = np.mean(X, axis=0)
        centered_X = X - self.mean 
        covariance = (1 / N) * np.dot(centered_X.T, centered_X)
        _, _, VT = np.linalg.svd(covariance)
        self.pca_components = VT[:num_components, :].T
        return self.pca_components

    def PCAMatrix(self, X):
        centeredX = X - self.mean
        reducedX = np.dot(centered_X, self.pca_components)
        return reduced_X

    def process(self, query_vector):
        preprocessed = self.preprocessor.getAllNormalizedData()
        filenames = []
        vectors = []
        for filename, data in preprocessed:
            filenames.append(filename)
            vectors.append(data)
        vectors = np.array(vectors)
        reduced_vectors = self.PCAMatrix(vectors)
        reduced_query = np.dot(query_vector - self.mean, self.pca_components)
        similarities = []
        for i, vec in enumerate(reduced_vectors):
            euclidean_dist = np.linalg.norm(reduced_query - vec)
            similarities.append((filenames[i], euclidean_dist))
        similarities.sort(key=lambda x: x[1])
        return similarities  

preprocessor = ImagePreprocessor((64, 64), "test")
preprocessor.preprocess()
processor = ImageProcessor("test")
normalized_data = []
filenames = []

for filename, data in preprocessor.getAllNormalizedData():
    filenames.append(filename)
    normalized_data.append(data)

normalized_data = np.array(normalized_data)
processor.PCAEigenVec(normalized_data)
query_vector = normalized_data[0] 

similarities = processor.process(query_vector)

for filename, distance in similarities[:5]: 
    print(f"{filename}")
