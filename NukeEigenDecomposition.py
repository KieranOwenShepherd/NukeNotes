try:
    import numpy as np
except ImportError:
    import sys
    sys.path.insert(0, "C:\Program Files\Side Effects Software\Houdini 16.0.671\python27\lib\site-packages")
    import numpy as np

import numpy.linalg as la

def sample_box(node, x_bounds, y_bounds, pixel_step, frame = None):
  if not frame:
    frame = nuke.frame()

  #set up progress
  t = nuke.ProgressTask('Sampling...') 
  for y in xrange( int(y_bounds[0]) , int(y_bounds[1]) , pixel_step ):

    if t.isCancelled():
      return
    t.setProgress(int(y/int(y_bounds[1])*100))


    samples = dict()

    #build dictionary (just convenient if we want to look up positions later) of samples
    for x in xrange( int(x_bounds[0]) , int(x_bounds[1]) , pixel_step ):
      samples[(x,y)] = [node.sample(c,x,y,frame) for c in ['r','g','b']] 

  del t
  return samples

box = nuke.selectedNode()['bbox']
samples = sample_box(  nuke.selectedNode(), (box.x() , box.r()) , (box.y() , box.t()), 1)

sample_array = np.array([v for n,v in samples.items()]).transpose()

print np.mean(sample_array, axis=0)

M = np.cov(sample_array)

print sample_array.shape

e, v = la.eig(M)
idx = np.argsort(e)[::-1]
e = e[idx]
e = np.real_if_close(e)
v = v[:, idx]

print M
print e
print v

