import numpy as np

def DiscreteWaveletTransform(discreteWave : list[float], maxdepth : int = -1) -> list[float]:
    '''Calculates the discrete wavelet transform up to maxdepth (-1 means no max depth)'''

    # Rounds up to power of 2
    if (len(discreteWave).bit_count() != 1):
        standardLength = 1 << len(discreteWave).bit_length()
    else:
        standardLength = len(discreteWave)
    
    discreteWave = discreteWave.copy()
    discreteWave.extend(0 for _ in range(standardLength - len(discreteWave)))
    midWave = [0 for _ in range(standardLength)]

    windowEnd = standardLength
    windowMid = standardLength // 2

    while maxdepth != 0 and windowEnd > 1:
        for i in range(0, windowEnd, 2):
            # High pass filter
            midWave[windowMid + i // 2] = (discreteWave[i] - discreteWave[i + 1]) / 2
        
        for i in range(0, windowEnd, 2):
            # Low pass filter
            midWave[i // 2] = (discreteWave[i] + discreteWave[i + 1]) / 2
        
        discreteWave = midWave.copy()
        windowEnd = windowMid
        windowMid //= 2
        maxdepth -= 1

    return discreteWave

def FastFourierTransformComplex(discreteWave : list[float]) -> list[float]:
    '''Calculates the fast fourier transform for all detectable frequencies in a discrete wave'''

    N = len(discreteWave)

    if N == 1: return discreteWave

    evenFFT = FastFourierTransformComplex(discreteWave[::2])
    oddFFT = FastFourierTransformComplex(discreteWave[1::2])

    factor = np.exp(-2j * np.pi * np.arange(N) / N)

    return np.concatenate([evenFFT + factor[:(N // 2)] * oddFFT, evenFFT + factor[(N // 2):] * oddFFT])

def FastFourierTransform(discreteWave : list[float]) -> list[float]:
    '''Calculates the fast fourier transform and returns the energy'''

    complexResult = FastFourierTransformComplex(discreteWave)

    return (np.pow(np.real(complexResult), 2) + np.pow(np.imag(complexResult), 2)).tolist()

def GenerateEnvelope(discreteWave : list[float]) -> list[float]:
    '''Generates the discrete envelope for a discrete wave'''

    return np.abs(discreteWave)

def FindTempo(discreteWave : list[float], sampleRate : int) -> float:
    '''Finds the tempo of a discrete wave given it's sample rate, this function assumes that the bpm will be in the 60-240 range'''

    waveEnvelope = GenerateEnvelope(discreteWave)

    maxCorrelation = 0
    bestbpm = 0

    for bpm in range(60, 241):
        shift = sampleRate * 60 // bpm

        correlation = np.sum(np.multiply(waveEnvelope, np.roll(waveEnvelope, shift)))

        if (correlation > maxCorrelation):
            maxCorrelation = correlation
            bestbpm = bpm
    
    return bestbpm
