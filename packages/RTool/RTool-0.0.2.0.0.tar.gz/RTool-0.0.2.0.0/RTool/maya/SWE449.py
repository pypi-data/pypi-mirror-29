'''RTool/maya/SWE449.py

SWE449 Midterm Project

This module is a combination of the different tools made for the
midterm project.

Todo:
    * Figure out how to setAttr for "defaultRenderGlobal" so that
        out rendering can be done.
    * Get ffmpeg to work in package natively...
    
Note:
    * In class, only sequenceToVideo will work since it doesn't use ffmpeg

Example:
    To test out the CreateVisualizer method in Maya, you must first import
    RTool properly. If RTool is installed using pip, simply type the
    following to be able to import in Maya::

        $ sys.path.append("C:/Python27/Lib/site-packages")
        $ sys.path.append("C:/Users/%s/AppData/Local/Programs/Python/Python36/Lib/site-packages"%getpass.getuser())

    Then simply::

        $ import RTool

    To test CreateVisualizer, you must have the path to a Wav file (wavPath)
    and use it as such::

        $ import RTool.maya.SWE449 as sw
        $ sw.CreateVisualizer(wavPath)
'''

import maya.cmds as mc
import pymel as pm
import MASH.api as mapi
import maya.mel as mel
import ntpath
import getpass

from RTool.maya.audio import AudioNode
import RTool.maya.util as util


wavPath = ("C:/Users/%s/Documents/maya/projects/default/sound/Keys_Noodle.wav"
    %getpass.getuser())

def CreateVisualizer(wavPath):
    '''Create a MASH visualizer in Maya given a Wav file path.

    Will create a new MASH network named "testNetwork", change the
    distribution type to 'grid' mode, add an audio node, set up the
    audio node, then change some variables to make it look interesting.

    Check module docstring for usage examples.

    Args:
        wavPath (str): The path to the Wav file to be used
    
    Notes:
        * Must be used in mayapy.exe
    
    '''
    mc.file(new=True, force=True)
    
    fileNameWithExtention = ntpath.basename(wavPath)
    fileName= fileNameWithExtention[:fileNameWithExtention.find(".")]
    
    cube = mc.polySphere()
    
    networkName = "testNetwork"
    mashNetwork = mapi.Network()
    mashNetwork.createNetwork(networkName)
    
    audioNode = AudioNode(mashNetwork, wavPath)
        
    #print(mc.getAttr(audioNode.name+".eqOutput"))
    
    mc.setAttr(audioNode.name+".scaleY", 100)
    
    mc.setAttr(networkName+"_Distribute"+".arrangement", 6) # 6 is Grid
    mc.setAttr(networkName+"_Distribute"+".gridAmplitudeX", 30)
    mc.setAttr(networkName+"_Distribute"+".gridAmplitudeZ", 10)
    mc.setAttr(networkName+"_Distribute"+".gridx", 30)
    
    colorNode = mashNetwork.addNode("MASH_Color")
    mc.setAttr(colorNode.name+".color", 0.222,0.222,0.888)
    
    colorFalloff = colorNode.addFalloff()
    mc.setAttr(colorFalloff+".falloffShape", 2) # 2 is Cube

def appendPackages():
    '''Paths to append in Maya for outside packages

    This is not to be used during runtime as a function. This is simply a
    reference to the paths to append in versions Python27 and Python36
    respectively. 
    
    '''
    sys.path.append("C:/Python27/Lib/site-packages")
    sys.path.append(
        "C:/Users/%s/AppData/Local/Programs/Python/Python36/Lib/site-packages"
            %getpass.getuser())

'''
def main():
    
        
if __name__ == "__main__":
    main()
'''
