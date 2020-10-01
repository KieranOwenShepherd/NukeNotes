import nuke

def swap_out_node(old, new, inputs=True, knobs=None):
    """swap the old nuke node out for the new node

    Args:
        old (nuke.Node): the node to swap out
        new (nuke.Node): the node to swap in
        inputs (bool, optional): connect inputs. Defaults to True.
        knobs (seq, optional): knobs to copy across. Defaults to None.
    """



def to_shuffle_copy(nk12_shuffle):
    shufflecopy = nuke.createNode('ShuffleCopy')

    swap_out_node(nk12_shuffle, shufflecopy)

    # set the shufflecopy channels
    for knob in ('in1', 'in2', 'out1', 'out2'):
        shufflecopy[knob].setValue(nk12_shuffle[knob].value())

    sh11_channels = ('red', 'green', 'blue', 'alpha') + ('red2', 'green2', 'blue2', 'alpha2')

    maps = nk12_shuffle['mapping'].getValue()

    sh11_inputs = (c for knob in ('in1', 'in2') for c in nuke.Layer(nk12_shuffle[knob].value()).channels())
    inputmap = dict(zip(sh11_inputs, sh11_channels))

    for i, channel in enumerate(sh11_channels):
        _, set_to, _ = maps[i]
        
        shufflecopy[channel].setValue(inputmap.get(set_to, default = set_to) )