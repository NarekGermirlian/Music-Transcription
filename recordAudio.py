import os
import pyaudio
import wave

def getRecordingNum() -> int:
    path = "Recordings"
    
    if not os.path.exists(path):
        os.makedirs(path)
    recordings = os.listdir(path)
    
    lastRecNum = 0
    if len(recordings)!=0:
        recordingNums=[]
        for i in range(len(recordings)):
            recordingNums.append(int(recordings[i][9:-4]))
    
        lastRecNum = max(recordingNums)

    return lastRecNum+1
    #for rec in os.listdir(path):
    #    recName = os.path.join(path, rec)
        

def record():
    # Sampling frequency (frames per second)
    FREQ = 44100

    # Start the stream
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=FREQ, input=True, frames_per_buffer=1024)
    
    frames = []

    # Wait for the user to press enter
    input("Press enter to start recording...")
    try:
        print("Recording started. Press CTRL+C to stop.")
        while True:
            # Record 1024 frames at a time
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)
    except KeyboardInterrupt:
        pass

    
    stream.stop_stream()
    stream.close()
    audio.terminate()

    file_dir_str = "Recordings/recording" + str(getRecordingNum()) + ".wav"
    sound_file = wave.open(file_dir_str, "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))

    print("Recording complete. Successfully wrote file in directory " + file_dir_str)
    return file_dir_str