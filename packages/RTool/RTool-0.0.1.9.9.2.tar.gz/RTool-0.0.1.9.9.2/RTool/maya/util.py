'''RTool/maya/util.py

'''

import maya.cmds as mc

def printAttr(node):
    for i in mc.listAttr(node):
        print(i)
