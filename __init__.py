# Connect anim curves, providing offset controls.
import maya.cmds as cmds

class Annotation(object):
    def __init__(s, obj, text):
        """ Create annotation """
        ann_shape = cmds.annotate(obj, tx=text)
        s.trans = cmds.listRelatives(ann_shape, p=True, pa=True)[0]
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

class Node(object):
    def __init__(s, name):
        s.node = cmds.shadingNode()
    def connect(s, from_, to):
        pass

def get_curves(obj_attr):
    """ Get anim curve from object attr """
    return cmds.listConnections(obj_attr, d=False, type="animCurve") or []

def controller(obj, attr):
    """ Create controller """
    obj_attr = "{}.{}".format(obj, attr)
    obj_curves = get_curves(obj_attr)
    if not obj_curves:
        raise RuntimeError("No animation curve found!")
    for curve in obj_curves:
        # Create control
        ctrl = Annotation(obj, "OFFSET")

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

        # Create output
        ctrl.add("Output", 0)

def main():
    controller(cmds.ls(sl=True)[0], "tx")
