import os
import struct
from PIL import Image

class NormalizedImageDataStream:
    '''Data stream for raw image data, should not be constructed manually.'''

    def __init__(self, source):
        self.dataSource = source
        self.files = [f for f in filter(lambda filename: filename.endswith(".nidat"), os.listdir(source.dir))]

    def __iter__(self) -> tuple[str, list[float]]:
        filename = self.files.pop(0)

        with open(os.path.join(self.source.dir, filename), "rb") as datafile:
            raw = datafile.read()
            dataSize = self.dataSource.targetDimenstion[0] * self.dataSource.targetDimension[1]
            data = list(struct.unpack('f' * dataSize, raw))

            return filename, data

class RawImageDataStream:
    '''Data stream for raw image data, should not be constructed manually.'''

    def __init__(self, source):
        self.dataSource = source
        self.files = filter(lambda filename: filename.endswith(".ridat"), os.listdir(source.dir))
    
    def __iter__(self) -> list[float]:
        filename = self.files.pop(0)

        with open(os.path.join(self.source.dir, filename), "rb") as datafile:
            raw = datafile.read()
            dataSize = self.dataSource.targetDimenstion[0] * self.dataSource.targetDimension[1]
            data = list(struct.unpack('f' * dataSize, raw))

            return filename, data

class ImagePreprocessor:
    '''Preprocessor for a specified image dimension and working directory. Used to get preprocessed image data.'''

    def __init__(self, dimension : tuple[int, int], dir : str):
        self.targetDimension = dimension
        self.directory = dir
    
    def generateRawImageDataFile(self, filename : str):
        '''Generates a raw image data file (.ridat) for the specified file in the preprocessor's working directory.'''

        pass

    def cleanRawImageDataFile(self, filename : str):
        '''Deletes the corresponding raw image data file (.ridat) of a specified file within the preprocessor's working directory.'''

        pass

    def getRawImageData(self, filename : str) -> list[float]:
        '''Retrieves the raw image data contained in the raw image data file (.ridat) of a specified file within the preprocessor's working directory.'''

        pass

    def generateRawImageDataFiles(self):
        '''Generates raw image data files (.ridat) for all image files within the preprocessor's working directory.'''

        pass

    def cleanRawImageDataFiles(self):
        '''Deletes all raw image data files (.ridat) within the preprocessor's working directory.'''

        pass

    def getAllRawImageData(self) -> RawImageDataStream:
        '''Retrieves raw image data contained in all raw image data files (.ridat) within the preprocessor's working directory in the form of a datastream.'''

        return RawImageDataStream(self)

    def generateDataAverageFile(self):
        '''Generates an average pixel data file (.apdat) for all image files within the preprocessor's working directory.'''

        pass

    def cleanDataAverageFile(self):
        '''Deletes the average pixel data file (.apdat) within the preprocessor's working directory.'''

        pass

    def getDataAverage(self) -> list[float]:
        '''Retrieves the average pixel data form the average pixel data file (.apdat) within the preprocessor's working directory.'''

        pass

    def generateNormalizedDataFile(self, filename : str):
        '''Generates a normalized data file (.nidat) for a specified file within the preprocessor's working directory.'''

        pass

    def cleanNormalizedDataFile(self, filename : str):
        '''Deletes the corresponding normalized data file (.nidat) of a specified file within the preprocessor's working directory.'''

        pass

    def getNormalizedData(self, filename : str) -> list[float]:
        '''Retrieves the normalized data from a specified file within the preprocessor's working directory.'''

        pass

    def generateNormalizedDataFiles(self):
        '''Generates normalized data files (.nidat) for every image file within the preprocessor's working directory.'''

        pass
    
    def cleanNormalizedDataFiles(self):
        '''Deletes all normalized data files (.nidat) within the preprocessor's working directory.'''

        pass

    def getAllNormalizedData(self) -> NormalizedImageDataStream:
        '''Retrieves normalized image data contained in all normalized image data files (.nidat) within the preprocessor's working directory in the form of a datastream.'''

        return NormalizedImageDataStream(self)

    def preprocess(self):
        '''Generates normalized data files (.nidat) for all image files and an average pixel data file (.apdat).'''

        self.generateNormalizedDataFiles()
        self.cleanRawImageDataFiles()

    def cleanAll(self):
        '''Deletes all files generated by the image preprocessor from it's working directory.'''

        self.cleanRawImageDataFiles()
        self.cleanDataAverageFile()
        self.cleanNormalizedDataFiles()

