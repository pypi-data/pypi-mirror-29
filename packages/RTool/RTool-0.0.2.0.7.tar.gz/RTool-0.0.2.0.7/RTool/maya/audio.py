'''RTool/maya/audio.py

Utility tools for Maya audio

Notes:
    * Must be run inside mayapy.exe !
    * Not to be confused with RTool.audio !
'''

import maya.cmds as mc
import MASH.api as mapi
import maya.mel as mel
import ntpath

def AudioNode(mashNetwork, filePath):
    '''Creates a MASH Audio node and sets it up correctly in Maya.

    This method creates and adds a new Mash Audio node to the given
    mashNetwork. It then sets the playback speed to real time, imports
    the audio file, adds it to the trax graph so it plays the audio, and
    then adds it to the MASH Audio node.

    Args:
        mashNetwork (str): The Maya string reference to a MASH network node.
        filePath (str): The path to an audio file.

    Returns:
        str: The Maya string reference to the created MASH Audio node.
    '''
    fileNameWithExtention = ntpath.basename(filePath)
    fileName= fileNameWithExtention[:fileNameWithExtention.find(".")]
    audioNode = mashNetwork.addNode("MASH_Audio")

    # sets playback to realtime
    mc.playbackOptions(edit=True, playbackSpeed=1, maxPlaybackSpeed=0)  

    # found that this is what Maya does in the background when done manually
    fileName = ''.join([i for i in fileName if not i.isdigit()])
    fileName = fileName.replace(' ', '_')
    
    mel.eval("file -import -type \"audio\"  -ignoreVersion -ra true -mergeNamespacesOnClash false -namespace \"%s\" -options \"o=0\"  -pr  -importTimeRange \"combine\" \"%s\";"
             %(fileName, filePath))
    mel.eval("doSoundImportArgList (\"1\", {\"%s\",\"0\"});"%(filePath))
    
    mc.setAttr(audioNode.name+".filename", filePath,type="string")
    return(audioNode)

