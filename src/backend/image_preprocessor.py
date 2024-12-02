import os
import struct
from PIL import Image
import numpy as np

class NormalizedImageDataStream:
    '''Data stream for raw image data, should not be constructed manually.'''

    def __init__(self, source):
        self.dataSource = source
        self.files = [f for f in filter(lambda filename: filename.endswith(".nidat"), os.listdir(source.directory))]

    def __iter__(self):
        return self

    def __next__(self) -> tuple[str, list[float]]:
        self.currentFile = self.files.pop(0)

        with open(os.path.join(self.source.directory, self.currentFile), "rb") as datafile:
            raw = datafile.read()
            dataSize = self.dataSource.targetDimenstion[0] * self.dataSource.targetDimension[1]
            self.currentData = list(struct.unpack('f' * dataSize, raw))

            return self.currentFile, self.currentData

class RawImageDataStream:
    '''Data stream for raw image data, should not be constructed manually.'''

    def __init__(self, source):
        self.dataSource = source
        self.files = filter(lambda filename: filename.endswith(".ridat"), os.listdir(source.directory))
    
    def __iter__(self):
        return self

    def __next__(self) -> list[float]:
        self.currentFile = self.files.pop(0)

        with open(os.path.join(self.source.directory, self.currentFile), "rb") as datafile:
            raw = datafile.read()
            dataSize = self.dataSource.targetDimenstion[0] * self.dataSource.targetDimension[1]
            self.currentData = list(struct.unpack('f' * dataSize, raw))

            return self.currentFile, self.currentData

class ImagePreprocessor:
    '''Preprocessor for a specified image dimension and working directory. Used to get preprocessed image data.'''

    def __init__(self, dimension : tuple[int, int], dir : str):
        self.targetDimension = dimension
        self.directory = dir

    def getAllFiles(self, extension : str) -> list[str]:
        '''Gets all files with a certain extension within the preprocessor's working directory.'''

        if extension.startswith('.'):
            fullExtension = extension
        else:
            fullExtension = '.' + extension

        return [f for f in filter(lambda filename: filename.endswith(fullExtension), os.listdir(self.directory))]

    def getAllImageFiles(self) -> list[str]:
        '''Gets all image files within the preprocessor's working directory.'''

        return [f for f in filter(lambda filename: any(filename.endswith(ext) for ext in Image.registered_extensions()), os.listdir(self.directory))]
    
    def generateRawImageDataFile(self, filename : str):
        '''Generates a raw image data file (.ridat) for the specified file in the preprocessor's working directory.'''

        filepath = os.path.join(self.dir, filename)

        with Image.open(filepath) as imageFile:
            resizedImage = imageFile.resize(self.targetDimension)
            rawData = np.array([list(resizedImage.getdata(0)), list(resizedImage.getdata(1)), list(resizedImage.getdata(2))])
            blackwhiteData = np.multiply([0.2989, 0.5870, 0.1140], rawData)

            with open(filepath + ".ridat", "wb") as outputFile:
                outputFile.write(struct.pack("f" * self.targetDimension[0] * self.targetDimension[1], *blackwhiteData))

    def cleanRawImageDataFile(self, filename : str):
        '''Deletes the corresponding raw image data file (.ridat) of a specified file within the preprocessor's working directory.'''

        filepath = os.path.join(self.dir, filename + ".ridat")
        if os.path.exists(filepath): os.remove(filepath)

    def getRawImageData(self, filename : str) -> list[float]:
        '''Retrieves the raw image data contained in the raw image data file (.ridat) of a specified file within the preprocessor's working directory.'''

        filepath = os.path.join(self.dir, filename + ".ridat")

        with open(filepath, "rb") as file:
            return list(struct.unpack("f" * self.targetDimension[0] * self.targetDimension[1], file.read()))

    def generateRawImageDataFiles(self):
        '''Generates raw image data files (.ridat) for all image files within the preprocessor's working directory.'''

        for imageFile in self.getAllImageFiles():
            self.generateRawImageDataFile(imageFile)

    def cleanRawImageDataFiles(self):
        '''Deletes all raw image data files (.ridat) within the preprocessor's working directory.'''

        for ridatFile in self.getAllFiles(".ridat"):
            os.remove(ridatFile)

    def getAllRawImageData(self) -> RawImageDataStream:
        '''Retrieves raw image data contained in all raw image data files (.ridat) within the preprocessor's working directory in the form of a datastream.'''

        return RawImageDataStream(self)

    def generateDataAverageFile(self):
        '''Generates an average pixel data file (.apdat) for all image files within the preprocessor's working directory.'''

        dataSum = np.zeros(shape=(self.targetDimension[0] * self.targetDimension[1]))
        dataCount = 0
        ridatFiles = self.getAllRawImageData()

        for pixelData in ridatFiles:
            dataCount += 1
            dataSum = np.add(dataSum, pixelData)
        
        if (dataCount == 0): return
        
        dataAverage = np.divide(dataSum, dataCount)

        with open("average.apdat", "wb") as file:
            file.write(struct.pack("f" * self.targetDimension[0] * self.targetDimension[1], *dataAverage))

    def cleanDataAverageFile(self):
        '''Deletes the average pixel data file (.apdat) within the preprocessor's working directory.'''

        if os.path.exists("average.apdat"): os.remove("average.apdat")

    def getDataAverage(self) -> list[float]:
        '''Retrieves the average pixel data form the average pixel data file (.apdat) within the preprocessor's working directory.'''

        with open("average.apdat", "rb") as file:
            return list(struct.unpack("f" * self.targetDimension[0] * self.targetDimension[1], file.read()))

    def generateNormalizedDataFile(self, filename : str):
        '''Generates a normalized data file (.nidat) for a specified file within the preprocessor's working directory.'''

        filepath = os.path.join(self.directory, filename)

        if not os.path.exists(filepath + ".nidat"): return

        denormalizedData = self.getRawImageData(filename)
        averageData = self.getDataAverage()
        normalizedData = np.subtract(denormalizedData, averageData)

        with open(filename + ".nidat", "wb") as nidatFile:
            nidatFile.write(struct.pack("f" * self.targetDimension[0] * self.targetDimension[1], *normalizedData))

    def cleanNormalizedDataFile(self, filename : str):
        '''Deletes the corresponding normalized data file (.nidat) of a specified file within the preprocessor's working directory.'''

        filepath = os.path.join(self.directory, filename + ".nidat")
        if os.path.exists(filepath): os.remove(filepath)

    def getNormalizedData(self, filename : str) -> list[float]:
        '''Retrieves the normalized data from a specified file within the preprocessor's working directory.'''

        filepath = os.path.join(self.directory, filename + ".nidat")

        with open(filepath) as file:
            return struct.unpack("f" * self.targetDimension[0] * self.targetDimension[1], file.read())

    def generateNormalizedDataFiles(self):
        '''Generates normalized data files (.nidat) for every image file within the preprocessor's working directory.'''

        for ridatFiles in self.getAllFiles(".ridat"):
            filename = ridatFiles.removesuffix(".ridat")
            self.generateNormalizedDataFile(filename)
    
    def cleanNormalizedDataFiles(self):
        '''Deletes all normalized data files (.nidat) within the preprocessor's working directory.'''

        for nidatFile in self.getAllFiles(".nidat"):
            os.remove(nidatFile)

    def getAllNormalizedData(self) -> NormalizedImageDataStream:
        '''Retrieves normalized image data contained in all normalized image data files (.nidat) within the preprocessor's working directory in the form of a datastream.'''

        return NormalizedImageDataStream(self)

    def preprocess(self):
        '''Generates normalized data files (.nidat) for all image files and an average pixel data file (.apdat).'''

        self.generateRawImageDataFiles()
        self.generateDataAverageFile()
        self.generateNormalizedDataFiles()
        self.cleanRawImageDataFiles()

    def cleanAll(self):
        '''Deletes all files generated by the image preprocessor from it's working directory.'''

        self.cleanRawImageDataFiles()
        self.cleanDataAverageFile()
        self.cleanNormalizedDataFiles()

