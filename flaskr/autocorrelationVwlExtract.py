# autocorrelation / energy at a certain point in speech should be high for a
# vowel <-- degree of voicing, usually > 0.25 for a vowel numpy correlate
# function to get autocorr (numpy.corr??) -->  array  r[t0] / r[0]

import numpy as np
import scipy.io.wavfile as wav

def extract_frame(data, rate, midTime_t, frame_size_ms=30):
    frame_size = int(rate * frame_size_ms / 1000)
    start_index = int(midTime_t * rate) - frame_size // 2
    end_index = start_index + frame_size
    frame = data[start_index:end_index]
    return frame

def autocorrelation(frame):
    result = np.correlate(frame, frame, mode='full')
    result = result[result.size // 2:]
    return result

def extractVwlBoundaries(filePath):
    # Example usage
    frameSize = 30

    # Plotting degree of voicing for visualization
    rate, data = wav.read(filePath)
    num_samples = len(data)
    data = data / num_samples
    duration = num_samples / rate
    time_stamps = np.arange(0, duration, frameSize / 1000)
    voicing_degrees = []

    for idx, time_t in enumerate(time_stamps):
        frame = extract_frame(data, rate, time_t, frameSize)
        if len(frame) == 0:
            voicing_degrees.append(0)
            continue
        autocorr = autocorrelation(frame)
        # print(idx, autocorr)
        voicingDegree = max(autocorr[1:])
        # print(idx,voicing_degree, '\n')
        voicing_degrees.append(voicingDegree)

    maxVD = max(voicing_degrees)
    voicing_degrees = voicing_degrees / maxVD
    # print(voicing_degrees)
    tOverThresh = []
    for i,vd in enumerate(voicing_degrees):
        if vd >= 0.2:
            tOverThresh.append(time_stamps[i])
    startT = tOverThresh[0]
    endT = tOverThresh[-1]
    frameSizeMs = (endT - startT) * 1000
    midT = (endT + startT) / 2
    print(frameSizeMs, startT,midT, endT)
    extractedData = extract_frame(data, rate, midT,frameSizeMs)
    newFile = filePath.replace('.wav','') + '-extractVwl.wav'
    wav.write(newFile,rate,extractedData)
    rate, data = wav.read(newFile)
    print(rate,data)
    return newFile, [startT,endT]