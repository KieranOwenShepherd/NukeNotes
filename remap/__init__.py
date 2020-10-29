    """Remap provides an object heirarchy matches that used in the nuke expressions syntax
    
    Each object is a dict-like container based on a nuke object with a thin object wrapping it.

    The nuke_api object can be accessed with .nukeobj

    It seems useful to provide a shortcut way to access objects using a dot separated path, 
    just like nuke expressions, so keying objects can also be done this way.
    """

import nuke
import _curveknob, _curvelib
import _splinewarp, _rotopaint
from collections import Mapping


# Each type of nuke object requires a unique object

def map_out(function, condition=True):
    """ a handy way to conditionally wrap the output in a class of function """
    def decorator(func):
        def wrapped(*args, **kwargs):
            if condition:
                return function(func(*args, **kwargs))
            else return func(*args, **kwargs)

class BaseMap(Mapping):
    """ Base map provides a way to store the underlying nuke object,
    and return the nukmber of elements __iter__ and __getitem__ still need to be implemented"""
    def __init__(self, nukeobj):
        self.nukeobj = nukeobj

    def __len__(self):
        return len(self.keys())


#----------------------------------------------------------------------------------------------

# Various knobs allow access of different attributes, 
# so we need a way to autowrap them

def node_factory(node):
    """ wraps to group if node is a group """
    return Group(node) if node.Class() == 'Group' else Node(node)

def knob_factory(knob):
    return {
        _rotopaint.RotoKnob:CurveKnob,
        _splinewarp.SplineKnob:CurveKnob
    }[type(knob)](knob)


class Group(BaseMap):
    def __iter__(self):
        return [n.name() for n in self.nukeobj.nodes()] + self.nukeobj.knobs().keys()

    @map_out(knob_factory, lambda o: type(o) == nuke.Knob)
    @map_out(node_factory)
    def __getitem__(self, key): 
        return self.nukeobj.node(key) or self.nukeobj.knob(key)

class Node(BaseMap):
    def __iter__(self): return [k.name() for k in self.nukeobj.knobs()]
    
    @map_out(knob_map)
    def __getitem__(self, key): return knob_factory(self.nukeobj.knob(key))


class Knob(BaseMap):
    def __iter__(self): self.nukeobj.names()
    def __getitem__(self, key): 

class CurveKnob(BaseMap):
    def __iter__(self): return Layer.__iter__(self.nukeobj.rootLayer)
    def __getitem__(self, key): return Layer.__getitem__(self.nukeobj.rootLayer)


# --------------- ROTOPAINT STRUCTURES ---------------

class Layer(BaseMap):
    def __iter__(self): return [item.name for item in self.nukeobj]
    def __getitem__(self, key): return next(item for item in self.nukeobj if item.name == key)

class Shape(BaseMap):
    atts = {
        'curve':ControlPointList,
        'curve_points':ControlPointList,
        'translate':lambda shape: Transform(shape.getTransform())
    }

    def __iter__(self): return self.atts.keys()
    def __getitem__(self, key): return self.atts[key](self.nukeobj)

class Transform(BaseMap):
    dim = {'x':0, 'y':1}

    def __iter__(self): return self.dim.keys()

    def __getitem__(self, key): 
        return self.nukeobj.getTranslationAnimCurve(self.dim[key])


class ControlPointList(BaseMap):

    def __iter__(self): return range(len(self.nukeobj))

    def __getitem__(self, key): return self.nukeobj[key]


class ControlPoint2D(BaseMap):
    dim = {'x':0, 'y':1}

    def __iter__(self): return self.dim.keys()

    def __getitem__(self, key): 
        return self.nukeobj.getPositionAnimCurve(self.dim[key])


class ControlPoint(BaseMap):
    
    # if type(self.nukeobj) is _curveknob.ShapeControlPoint:
    #         return dict(
    #             main = base.center,
    #             left = base.leftTangent,
    #             right = base.rightTangent,
    #             feather_main = base.feathercenter,
    #             feather_left = base.featherLetfTangent,
    #             feather_right = base.featherRightTangent
    #         )[key]
    #     if type(self.nukeobj) is _curvelib.AnimControlPoint
    #         return self.nukeobj # whatever is asked for only return main
    def __iter__(self): return None

    def __getitem__(self, key): return NOne
        

class AnimCurve(BaseMap):
    def __iter__(self): return None
    def __getitem__(self, key): return None


#--------------------------------------------------------------------------------------------------

def root():
    """ root is exactly like a group node """
    return Group(nuke.Root())