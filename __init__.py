# Connect anim curves, providing offset controls.
import maya.cmds as cmds

class Node(object):
    def __init__(s, transform):
        s.trans = transform
        for a in ("t", "r", "s"):
            for b in ("x", "y", "z"):
                cmds.setAttr(s._attr(a, b), k=False, cb=False)
    def add(s, attr, val):
        """ Add numeric attribute to object """
        cmds.addAttr(s.trans, ln=attr, dv=val)
        cmds.setAttr(s._attr(attr), k=True)

    def set(s, attr, val, time=None, **kwargs):
        """ Set value on attribute """
        time = cmds.currentTime(q=True) if time is None else time
        cmds.setKeyframe(s._attr(attr), v=val, t=time, **kwargs)

    def get(s, attr, *args, **kwargs):
        """ Get attr """
        return cmds.getAttr(s._attr(attr), *args, **kwargs)

    def __str__(s): return s.trans
    def _attr(s, *attrs): return "{}.{}".format(s.trans, "".join(attrs))

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
    ctrl = annotate(obj, "OFFSET")
    obj_attr = "{}.{}".format(obj, attr)

    # Get frame range
    in_frame = cmds.playbackOptions(q=True, min=True)
    out_frame = cmds.playbackOptions(q=True, max=True)

    # Create Init attr
    ctrl.add("Init", cmds.getAttr(obj_attr, t=in_frame))

    # Create timewarp
    ctrl.add("Time", 0)
    ctrl.set("Time", in_frame, in_frame, ott="linear")
    ctrl.set("Time", out_frame, out_frame, itt="linear")

    # Create scale
    ctrl.add("Scalar", 1)

    # Create offset
    ctrl.add("Offset", ctrl.get("Init"))

def main():
    controller(cmds.ls(sl=True)[0], "tx")
