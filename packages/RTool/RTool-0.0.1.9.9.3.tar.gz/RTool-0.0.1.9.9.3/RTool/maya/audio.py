'''RTool/maya/audio.py

Utility tools for maya audio

Notes:
    * Must be run inside mayapy.exe !
'''

import maya.cmds as mc
import MASH.api as mapi
import maya.mel as mel
import ntpath

def AudioNode(mashNetwork, filePath):
    '''

    '''
    fileNameWithExtention = ntpath.basename(filePath)
    fileName= fileNameWithExtention[:fileNameWithExtention.find(".")]
    audioNode = mashNetwork.addNode("MASH_Audio")
    
    mc.playbackOptions(edit=True, playbackSpeed=1, maxPlaybackSpeed=0) # sets playback to realtime 
    
    mel.eval("file -import -type \"audio\"  -ignoreVersion -ra true -mergeNamespacesOnClash false -namespace \"%se\" -options \"o=0\"  -pr  -importTimeRange \"combine\" \"%s\";"%(fileName,filePath))
    mel.eval("doSoundImportArgList (\"1\", {\"%s\",\"0\"});"%(filePath))
    
    mc.setAttr(audioNode.name+".filename", filePath,type="string")
    return(audioNode)

