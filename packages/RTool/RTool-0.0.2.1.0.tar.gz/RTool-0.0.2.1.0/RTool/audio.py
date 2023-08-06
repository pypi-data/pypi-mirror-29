'''RTool/audio.py

This module is a combination of various audio relation functions. Anything
that doesn't go into video.py goes in here. This will include funtions like
converting audio from one type to another, etc.

Note:
    * Not to be confused with RTool.maya.audio !!

'''
import os, subprocess

def convertToWav(originalFilePath, savePath):
    '''Convert an acceptable audio file into a Wav file.

    This function creates a Wav file out of any acceptable audio file type
    and names it the same name then saves it in the savePath.

    Args:
        originalFilePath (str): The path to the file being converted.
        savePath (str): The directory path in which to save the Wav file.

    Attributes:
        acceptable (str[]): The string array of acceptable extensions.

    Returns:
        str: The path to the newly created Wav file.
        
    Note:
        *Prevention of loss of quality is not assured.

    Todo:
        * Make acceptable list work
    '''
    acceptable = ['flac','mp3']

    fileNameWithExtention = os.path.basename(originalFilePath)
    fileName = fileNameWithExtention[:fileNameWithExtention.find(".")]

    wavPath = os.path.join(savePath, fileName+'.wav')
    command = ("ffmpeg -i \"%s\" \"%s\""
               %(originalFilePath, wavPath))

    print(subprocess.call(command, shell=True))
    
    return wavPath

    
