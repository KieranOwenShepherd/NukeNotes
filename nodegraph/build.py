
import nuke

def get_input_connections(node):
    """the inputs of a node and the input number it's connected to

    Args:
        node (nuke.Node): a nuke node

    Yields:
        (node, int): a nuke node and the input number connected
    """    
    for i in range(node.inputs()):
        yield node.input(i), i


def get_output_connections(node):
    """get the nodes connected to the output of this node
    and the input numbers it's connected to

    Args:
        node (nuke.Node): a nuke node

    Yields:
        (node, tuple(int)): a connected node and the input that's connected
    """    
    for n in node.dependent(nuke.INPUTS):
        yield n, tuple(i for i in range(n.inputs()) if n.input(i) is node)


def swap_out_node(old, new, knobs=('xpos', 'ypos')):
    """swap the old nuke node out for the new node,
    optionally copying knob values intothe new knob.
    you should be careful not to copy python knobs on custom nodes
    (PyCustom_Knob, PyScript_Knob, PythonCustomKnob, PythonKnob)

    Args:
        old (nuke.Node): the node to swap out
        new (nuke.Node): the node to swap in
        knobs (seq, optional): knobs to copy across. Defaults to None.
    """
    for node, i in get_input_connections(old):
        new.setInput(i,node)
    
    for node, connected_inputs in get_output_connections(old):
        for i in connected_inputs:
            node.setInput(i,new)

    for knob in knobs:
        new.knob(knob).fromScript(old.knob(knob).toScript())

