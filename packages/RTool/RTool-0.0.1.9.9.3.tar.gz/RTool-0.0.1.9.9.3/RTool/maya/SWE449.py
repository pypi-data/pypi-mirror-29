'''RTool/maya/SWE449.py

SWE449 Midterm Project

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

def main():
    sys.path.append("C:/Python27/Lib/site-packages")
    sys.path.append(
        "C:/Users/%s/AppData/Local/Programs/Python/Python36/Lib/site-packages"
            %getpass.getuser())

def CreateVisualizer(wavPath):
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
    mc.setAttr(colorNode.name+".color", 1,0.654,0.654)
    
    colorFalloff = colorNode.addFalloff()
    mc.setAttr(colorFalloff+".falloffShape", 2) # 2 is Cube
        
if __name__ == "__main__":
    main()
