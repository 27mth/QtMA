import maya.cmds as cmds
import maya.mel as mel

# Define the global variable 'selected'
selected = cmds.ls(selection=True)

def shaderChange():
    # change the shaders of the selected objects into aiStandardSurface
    for obj in selected:
        # create a new aiStandardSurface shader
        aiStandardSurface = cmds.shadingNode('aiStandardSurface', asShader=True)
        # assign the new aiStandardSurface shader to the selected objects
        cmds.select(obj)
        cmds.hyperShade(assign=aiStandardSurface)
        # connect the outColor of the new aiStandardSurface to the surfaceShader of the shadingEngine
        shadingEngines = cmds.listConnections(obj, type='shadingEngine')
        if shadingEngines:
            for shadingEngine in shadingEngines:
                cmds.connectAttr(aiStandardSurface + '.outColor', shadingEngine + '.surfaceShader')
        # rename the obj's vertex color set and check the new name is unique
        renamedColorSet = 'newColorSet'
        i = 1
        while renamedColorSet in cmds.polyColorSet(obj, query=True, allColorSets=True):
            renamedColorSet = 'newColorSet' + str(i)
            i += 1
        #rename the original vertex color set to the new name
        cmds.polyColorSet(rename=True, newColorSet= renamedColorSet)

        # create a new aiUserDataColor node and set attribute 'attribute' to colorSet
        aiUserDataColor = cmds.shadingNode('aiUserDataColor', asTexture=True)
        cmds.setAttr(aiUserDataColor + '.attribute', renamedColorSet, type='string')
        # create a new aiMultiply node and connect the new aiUserDataColor node to the aiMultiply node's input1
        aiMultiply = cmds.shadingNode('aiMultiply', asTexture=True)
        cmds.connectAttr(aiUserDataColor + '.outColor', aiMultiply + '.input1')
        # connect the new aiMultiply node to the base color of the aiStandardSurface
        cmds.connectAttr(aiMultiply + '.outColor', aiStandardSurface + '.baseColor')

def deleteUnusedNodes():
    # delete unused nodes
    mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')

def vertColorOn():
    # change the selected objects' shape node attribute '.aiExportColor' to 1
    for obj in selected:
        shapes = cmds.listRelatives(obj, shapes=True)
        if not shapes:
            continue
        for shape in shapes:
            mel.eval('setAttr "' + shape + '.aiExportColors" 1;')

# Check if selected is empty
if not selected:
    print('Please select some objects.')
else:
    vertColorOn()
    shaderChange()
    deleteUnusedNodes()