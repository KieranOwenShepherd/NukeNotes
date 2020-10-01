import nuke

from nodegraph import build



def to_shuffle_copy(nk12_shuffle):
    shufflecopy = nuke.createNode('ShuffleCopy')

    build.swap_out_node(nk12_shuffle, shufflecopy)

    # set the shufflecopy channels
    for new_k, old_k in zip(('in', 'in2', 'out', 'out2'),('in1', 'in2', 'out1', 'out2')):
        shufflecopy[old_k].setValue(nk12_shuffle[new_k].value())

    # set the shuffle copys selectors
    inputmap = dict(zip(
        (c for knob in ('in1', 'in2') for c in nuke.Layer(nk12_shuffle[knob].value()).channels()), 
        ('red', 'green', 'blue', 'alpha') + ('red2', 'green2', 'blue2', 'alpha2')
    ))

    maps = nk12_shuffle['mappings'].value()
    sh11_out_selectors = ('red', 'green', 'blue', 'alpha') + ('black', 'white', 'red2', 'green2') # the bizarre names for the shuffles selector knobs
    for m, channel in zip(maps, sh11_out_selectors): 
        shufflecopy[channel].setValue(inputmap.get(m[1], default = m[1]) )