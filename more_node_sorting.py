#now, any clump that we can make seems to make sense that that should be treated as a superset also

#supersets - should have <= 1 input <= 1 output

#as long as a set of nodes has only one input and output, we can clump them together
#any nodes with no inputs can be a little further away
def clump(nodes):
    def atop(node, below_node, distance):
        node.setXYpos(below.x,below.y+distance)
        #also need to account for node height
    if len(outputs(node)) == 1:
        below = output_map(node)[0]
        if len(inputs(below)) == 1:
            if inputs(node) == 0:
                #give it a little more room
                atop(node, below, -40)
            else:
                atop(node, below, -20)