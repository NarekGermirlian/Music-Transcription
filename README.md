# Project Description 
This program is a tool that provides a transcription of notes given an audio recording, created by the user. This program uses artificial intelligence to recognize the notes, and can be useful to for a variety of reasons:
* Checking the tune of an instrument
* Confirming whether you're singing in tune
* General transcription of a melody

# Instructions to run
Python version == 3.10.14

Install all dependencies in requirements.txt. Note that requirements.txt is meant for macs using silicon chips. 
However, on any other platform, ensure that tensorflow version >= 2.0.0 is installed in the ran environment, along with the depenencies listed in requirements.txt.

If ran on a mac, ensure tensorflow is installed correctly. More information can be found [here](https://www.tensorflow.org/install/pip) for intel chips and [here](https://gist.github.com/svpino/31a16d236ca730336c54e3581f5c5b1b) for silicon chips

To run the program, run main.py. The program will be interacted via the console.

## When it works best
The program works best with slow, single melodies with no background noise or tracks. As a good rule of thumb, if a melody can be hummed clearly, the program will run well.
