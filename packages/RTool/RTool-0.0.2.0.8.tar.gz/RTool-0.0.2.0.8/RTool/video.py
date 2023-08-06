'''RTool/video.py

This module is a combination of various video related functions for
converting sequences to video, vise-versa, extracting audio, etc.

Most of these functions work based on directory paths since that was
the functionality needed when these were written.

Todo:
    * Auto-handle directories creation
    * Combined methods
    * Fix mp4ToWav, check Notes
    * Auto-handle conflicts
'''

from __future__ import division
from ntpath import basename
import subprocess, sys, os

from RTool.util.importer import ImportHandler
exec(ImportHandler(["imageio","PIL"]))

from PIL import Image, ImageStat

rootPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(os.path.split(rootPath)[0],"ffmpeg","bin"))

def sequenceToVideo(dirPath, vType="mp4", fps=24):
    '''Turn a directory of an image sequence into a video format.

    Args:
        dirPath (str): The path to the directory of the image sequence.
        vType (str): The video extension to use. Defaults to 'mp4' but
            can be changes to 'gif'.
        fps (int): The frames-per-second rate of the video. Defaults
            to 24.

    Returns:
        string: The path to the created video file.
    '''
    dirList = os.listdir(dirPath)
    os.chdir(dirPath)

    fileName = ('%s.%s'
        %(os.path.join(dirPath, os.path.basename(dirPath)), vType))
    writer = imageio.get_writer(fileName, fps=fps)

    dirListLength = len(dirList)
    fifth = int(round(dirListLength/20))
    subindex = 0

    index = 0
    imgs = []
    for i in dirList:
        if (i[i.rfind('.')+1:] in acceptableExtensions):
            #print(Image.open(os.path.join(dirPath, i)).size)
            imgs.append(imageio.imread(os.path.join(dirPath, i)))
            writer.append_data(imgs[index])

            index += 1

        if ((fifth < 50) and (index % fifth == 0)) or (index % 50 == 0):
            print("sequenceToMP4: %d/%d || %04.2f%% || %s"
                  %(index, dirListLength, index/dirListLength*100, stopwatch.current()))
        subindex+=1

    writer.close()
    print("sequenceToMP4: %d/%d || 100%%"
          %(dirListLength,dirListLength))

    videoPath = os.path.join(dirPath, fileName)
    return videoPath

def mp4ToSequence(videoPath, outDir=rootPath):
    '''Turn an mp4 into an image sequence.

    Args:
        videoPath (str): The path to the video file.
        outDir (str): The path to the output directory. This should be
            an empty folder so that the images can save with no conflict.

    Returns:
        int: The frames-per-second rate of the video file.
    '''
    videoNameWithExtension = os.path.basename(videoPath)
    videoName = videoNameWithExtension[:videoNameWithExtension.find(".")]
    reader = imageio.get_reader(videoPath, 'ffmpeg')
    readerLength = len(reader)
    fifth = int(round(readerLength/20))
    padding = len(str(readerLength))
    try:
        for i, im in enumerate(reader):
            #print(i, im)
            writer = imageio.get_writer(
                os.path.join(outDir, videoName+"_"+str(i).zfill(padding)+".png"))
            writer.append_data(im)
            writer.close()

            if ((fifth < 25) and (i % fifth == 0)) or (i % 25 == 0):#i % fifth == 0:
                print("mp4ToSequence: %d/%d || %04.2f%% || %s"
                      %(i,readerLength,i/readerLength*100,stopwatch.current()))
    except:
        print("ERROR in mp4ToSequence: frame could not be read.")

    print("mp4ToSequence: %d/%d || 100%%"%(readerLength,readerLength))

    fps = reader.get_meta_data()['fps']
    return fps

def mp4ToWav(videoPath, wavName="audio.wav", savePath=rootPath):
    '''Extract mp4 file from video file.

    Args:
        videoPath (str): The path to the video file.
        wavName (str): The name of the Wav file to be created.
            Defaults to 'audio.wav'.
        savePath (str): The diretory path to save the Wav file in.
            Defaults to rootPath of script.

    Returns:
        str: The path to the newly created Wav file.
        
    Notes:
        * Doesn't work if file already exists, freezes program.
    '''
    wavPath = os.path.join(savePath, wavName)
    command = ("ffmpeg -i \"%s\" -ab 160k -ac 2 -ar 44100 -vn \"%s\""
               %(videoPath, wavPath))
    subprocess.call(command, shell=True)
    return wavPath

def mapWavToMP4(wavPath, mp4Path):
    '''Maps a Wav audio file to a video file.

    Creates the newly formed mp4 video file in the same directory as
    the original but renames to have the prefix 'audio_'.
    
    Args:
        wavPath (str): The path to the Wav audio file.
        mp4Path (str): The path to the mp4 video file.

    Returns:
        str: The path to the newly created mp4 video/audio file.
    '''
    mp4Name = os.path.basename(mp4Path)
    newMP4Path = os.path.join(os.path.dirname(mp4Path),"audio_"+mp4Name)
    
    # was working, not anymore...
    command = ("ffmpeg -i \"%s\" -i \"%s\" -vcodec copy -acodec copy \"%s\""
               %(mp4Path, wavPath, newMP4Path))

    # currently working
    commnd2 = ("ffmpeg -i \"%s\" -i \"%s\" -c:v copy -c:a aac -strict experimental \"%s\""
               %(mp4Path, wavPath, newMP4Path))
    
    subprocess.call(commnd2, shell=True)
    return newMP4Path

def getMP4FPS(videoPath):
    '''Get the frames-per-second rate of a video file.

    Args:
        videoPath (str): The path to a video file.

    Returns:
        int: The frames-per-second of the video file.
    
    Notes:
        * Only use when sequence already created, otherwise mp4ToSequence
            already returns fps.
    '''
    reader = imageio.get_reader(videoPath, 'ffmpeg')
    fps = reader.get_meta_data()['fps']
    return fps
