# Connect anim curves, providing offset controls.
import maya.cmds as cmds

def annotate(obj, text):
    """ Create annotation """
    ann_shape = cmds.annotate(obj, tx=text)
    ann = cmds.listRelatives(ann_shape, p=True, pa=True)[0]
    for a in ("t", "r", "s"):
        for b in ("x", "y", "z"):
            cmds.setAttr("{}.{}{}".format(ann, a, b), k=False, cb=False)
    return ann


def main():
    annotate(cmds.ls(sl=True)[0], "something!")
