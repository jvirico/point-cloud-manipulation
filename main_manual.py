import numpy as np
import my_utils as mine
import os


filename = './data/shepplogan.pgm3d'
labels = 5

mesh = mine.GetMesh(filename, labels)
mesh_obj = mine.MeshToOBJ(mesh)
# saving mesh to obj file
f = open(os.path.filename(filename) + '.obj','w')
f.write(mesh)
f.close()
