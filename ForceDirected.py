from threading import Thread
from itertools import permutations
from itertools import groupby
import time
import math

def p(n):
    return nuke.math.Vector2(n.xpos(),n.ypos())

def setpos(node, p):
    node.setXYpos(int(p.x),int(p.y))

def pushnode(node, push):
    setpos(node, p(node)+push)

#pushes nodes away from each other
#gives force on p1 from p2
def coulomb_force(p1,p2):
    A = 1.0/150.0 #sets the falloff
    B = 1.0/5 #sets the absolute maximum coulomb force
    distsquared = p1.distanceSquared(p2) #don't allow zero
    return -(p2-p1)*1/(A*distsquared+B)

#pulls nodes toward each other
#gives force on p1 from p2
#this is balanced so that the spring constant always gives a proportion of the distance that the node will move
def spring_force(p1,p2,relaxed_length):
    distance = p1.distanceBetween(p2)
    force = 0.3*(distance-relaxed_length)/(distance+0.0000001) #don't allow zero
    return (p2-p1)*min(force,20)

#stacking force
#this opposes the general float force
def stacking_force(p1,p2):
    vector = p2-p1
    return nuke.math.Vector2( vector.y*2 , 0 )

#test for below-ness
def is_below(p1,p2):
    return -(p2-p1).y > 0



def force_directed(t, nodes):
    output_map   = { n:n.dependent(nuke.INPUTS,False) for n in nodes}
    input_map    = { n:n.dependencies(nuke.INPUTS)    for n in nodes}
    total_forces = { n:nuke.math.Vector2(0,0) for n in nodes}
    down_anchors = [n for n,out in output_map.items() if len(out) == 0]
    up_anchors   = [n for n,inp in input_map.items()  if len(inp) == 0]

    while t > 0:

        for n in nodes:
            total_forces[n].set(0,0)

        #apply coulomb
        for n,c in permutations(nodes,2):
            if n in up_anchors + down_anchors:
                continue
            total_forces[n] += coulomb_force(p(n),p(c))
            if 'Const' in n.name():
                print n.name()

        #apply springs
        for n in nodes:
            for c in input_map[n]:
                total_forces[n] += spring_force(p(n),p(c),200)

            for c in output_map[n]:
                total_forces[n] += spring_force(p(n),p(c),200)

        #apply string straightening
        for n in up_anchors:
            total_forces[n].y -= 50/len(up_anchors)
        for n in down_anchors:
            total_forces[n].y += 50/len(down_anchors)

        #alignment supersets
        #if nodes are connected and alined, 
        #treat them as a superset
        supersets = []
        super_map = dict()
        def connected_and_aligned_y(n1,n2):
            return n1 in input_map[n2] + output_map[n2] and p(n1).x == p(n2).x
        for n,c in permutations(nodes,2):
            if connected_and_aligned_y(n,c):
                if n in super_map:
                    super_map[n].append(c)
                else:
                    new_set = [n,c]
                    supersets.append(new_set)
                    super_map[n] = new_set
        for s in supersets:
            x = sum(total_forces[n].x for n in s)/len(s)
            for n in s:
                pass
                #total_forces[n].x = x
                

        for n in nodes:
            pushnode(n,total_forces[n])

        nuke.executeInMainThread(lambda: None)
        t -= 1
        time.sleep(0.002)


# Create and launch a thread
t = Thread(target=force_directed, args=(200, nuke.selectedNodes()))
t.start()