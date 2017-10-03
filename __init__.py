# Connect anim curves, providing offset controls.
import maya.cmds as cmds

class Node(object):
    def __init__(s, transform):
        s.trans = transform
        for a in ("t", "r", "s"):
            for b in ("x", "y", "z"):
                cmds.setAttr("{}.{}{}".format(transform, a, b), k=False, cb=False)
    def add(s, attr, val):
        """ Add numeric attribute to object """
        cmds.addAttr(s.trans, ln=attr, dv=val)
        cmds.setAttr("{}.{}".format(s.trans, attr), k=True)

    def set(s, attr, *args, **kwargs):
        """ Set value on attribute """
        cmds.setAttr("{}.{}".format(s.trans, attr), *args, **kwargs)

    def get(s, attr, *args, **kwargs):
        """ Get attr """
        return cmds.getAttr("{}.{}".format(s.trans, attr), *args, **kwargs)

    def __str__(s):
        return s.trans

def annotate(obj, text):
    """ Create annotation """
    ann_shape = cmds.annotate(obj, tx=text)
    ann = cmds.listRelatives(ann_shape, p=True, pa=True)[0]
    for a in ("t", "r", "s"):
        for b in ("x", "y", "z"):
            cmds.setAttr("{}.{}{}".format(ann, a, b), k=False, cb=False)
    return Node(ann)

def controller(obj, attr):
    """ Create controller """
    ann = annotate(obj, "OFFSET")
    print "{}".format(ann)
    cmds.select(ann)
    # add(ann, "Init", cmds.getAttr())
    # add(ann, "Time", 0)
    # add(ann, "Scalar", 0)
    # add(ann, "Offset", 0)

def main():
    controller(cmds.ls(sl=True)[0], "tx")
