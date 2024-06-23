import crepe
from scipy.io import wavfile
import numpy as np
import sys
import logging

from recordAudio import record

# Remove logging of tensorflow
logging.getLogger("tensorflow").setLevel(logging.FATAL)

CHANGE_CONSTANT = (2 ** (1/12)) - 1  #Approximately 0.0595
MIN_CHANGE_FREQ = 0.05 #Adjusted for human error in singing

def getTimeFreqConf(recording: str, minConfidence: float=0.6, step: int=100) -> np.ndarray[any]:
    """
    Get a numpy 2D Array with corresopnding Time, Frequency, and Confidence columns

    Parameters
    ----------
    recording : str
        The .wav audio file to analyze
    minConfidence : float
        The minimum confidence of correct pitches to include. Default value of 0.6
    step : int (ms)
        How often in the sample is the pitch measured

    Returns
    -------
    np.ndarray[any]
        The numpy 2D Array

    Raises
    ------
        ArgumentOutOfRangeException : if the str is not of .wav format
    """
    sr, audio = wavfile.read(recording)
    time, frequency, confidence, activation = crepe.predict(audio, sr, viterbi=True, step_size=step)

    a2D = np.column_stack((time, frequency, confidence))
    return a2D[(confidence>minConfidence)]

def isChangeOfNote(freq1: float, freq2:float) -> bool:
    return abs((freq2-freq1)/freq1)>=MIN_CHANGE_FREQ

def getNextFreq(startFreq: float) -> float:
    return startFreq + (startFreq*CHANGE_CONSTANT)

def getMeanFreqs(freqs: np.ndarray) -> np.ndarray:
    means = []

    currCount=1
    currSum=freqs[0][1]

    currMean = freqs[0][1]
    currMeanStartTime = freqs[0][0]
    currMeanEndTime = -1
    for i in range(1, len(freqs)):
        # If we finished iterating, include last item in our calculations
        if (i==len(freqs)-1):
            currMeanEndTime=freqs[i][0]
            currSum+=freqs[i][1]
            currCount+=1
            currMean=currSum/currCount

            means.append([currMeanStartTime, currMeanEndTime, currMean])
        #If there is a change in note betwwen this and the previous note
        # OR we finished iterating
        # -> restart the mean value
        elif isChangeOfNote(freqs[i-1][1], freqs[i][1]):
            currMeanEndTime=freqs[i-1][0]
            means.append([currMeanStartTime, currMeanEndTime, currMean])
            
            currCount=1
            currSum=freqs[i][1]
            currMean=freqs[i][1]
            currMeanStartTime=freqs[i][0]
        
        #If there is no change in note, update the running mean
        else:
            currCount+=1
            currSum+=freqs[i][1]
            currMean=(currSum/currCount)

    return np.array(means)

def filterFreqs(freqs: np.ndarray, minInterval: float=0.15):
    filteredMeans: list = []
    #First, filter out list so that only notes with minInterval are included
    for i in range(0, len(freqs)):
        row=freqs[i]
        if abs(row[1]-row[0])>=minInterval:
            filteredMeans.append(freqs[i])
    return filteredMeans

def getNotesFreqs() -> list:
    oneOctave=["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    C0FREQ=16.3515978313
    freq=C0FREQ

    octave=0
    notes=[]
    for i in range(9):
        for noteName in oneOctave:
            notes.append([freq, noteName+str(octave)])
            freq=getNextFreq(freq)
        octave+=1
    return notes

def getNotesFromMeans(means: np.ndarray) -> np.ndarray:
    #Match corresponding frequencies to notes
    noteFreqs: list = getNotesFreqs()
    notes=[]
    for i in range(len(means)):
        freq = means[i][2]

        minDiff : float = sys.float_info.max
        minDiffNote : str = "C0"
        for r in range(len(noteFreqs)):
            realFreq=noteFreqs[r][0]
            if (abs(realFreq-freq)<minDiff):
                minDiff=abs(realFreq-freq)
                minDiffNote=noteFreqs[r][1]

        startTime = means[i][0]
        endTime = means[i][1]
        notes.append([startTime, endTime, minDiffNote])

    return notes

recording_dir = record()
freqs = getTimeFreqConf(recording=recording_dir, minConfidence=0.85, step=100)
meansFreqs = getMeanFreqs(freqs)
filteredFreqs = filterFreqs(meansFreqs)
notes = getNotesFromMeans(filteredFreqs)

# Print out the notes
if len(notes)!=0:
    print([note[2] for note in notes])
else:
    print("No notes detected.")