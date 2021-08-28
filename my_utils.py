##############################################
## Author:  Javier R. 
## Contact: jvirico@gmail.com
##          https://github.com/jvirico
##############################################


import os
import numpy as np
from tqdm import trange

####
##  Utils for PGM3D files
#
### File metadata exploration and data conversion
'''
    .pgm3d format inludes a 3 line header:
        PGM3D       <- file_format
        64 64 64    <- size of 3D image
        255         <- max gray level
        0           <- data starts
'''

def convert_line_to_size(size_line):
    '''
        returns size of 3D image form str
    '''
    size=size_line.split(" ")
    size[-1]=size[-1].split("\n")[0]
    for i in range(len(size)):
        size[i]=int(size[i])
    return size


def PGM3D_GetMetadata(filename='./data/shepplogan.pgm3d'):
    '''
        extracts size info from file header and converts it to 
        a 3D numpy array
    '''

    data = open(filename,'r')
    file_format = data.readline() # PGM3D in this case
    size_line = data.readline()
    size = convert_line_to_size(size_line) # size of 3D image
    print('The volume has size %s'%size)
    max_value = int(data.readline()) # max gray level
    data.close()
    ### End of 'File metadata exploration'

    ### Converting data to 3D numpy array for future manipulation
    val = np.loadtxt(filename,dtype=np.int32, skiprows=3)
    #print('Raw data: %s'% val[:20])
    val_mat = val.reshape([size[0],size[1],size[2]])
    #print(val_mat[0])
    return val_mat, max_value


def Mesh_To_OBJ(vertices, faces, obj_filename):
    '''
        OBJ files allow to describe a 3D mesh from a list of vertices and faces
            # list of all vertices
            v x1 y1 z1
            v x2 y2 z2
            v x3 y3 z3
            ...
            v xN yN zN
            # list of faces (triangles)
            f 1 2 3
        ...
    '''
    f = open(obj_filename,'w')
    assert vertices.shape[1] == 3
    assert faces.shape[1] == 3
    for i in range(vertices.shape[0]):
        f.write("v "+str(vertices[i, 0])+" "+str(vertices[i, 1])+" "+str(vertices[i, 2])+"\n")
    for j in range(faces.shape[0]):
        f.write("f "+str(faces[j, 0])+" "+str(faces[j, 1])+" "+str(faces[j, 2])+"\n")
    f.close()


# Testing OBJ generation
def TEST_01():
    dst_file = './out/test.obj'
    vertices = np.array([[0,0,0],[0,1,0],[1,1,0],[1,0,0],[0,1,1],[0,0,1],[1,1,1],[1,0,1]])
    faces = np.array([[1,2,3],[1,3,4],[4,3,7],[4,7,8],[8,7,6],[5,6,7],[1,6,5],[5,2,1],[2,5,3],[3,5,7],[1,4,6],[4,8,6]])
    Mesh_To_OBJ(vertices,faces,dst_file)
    print('TEST_01: OBJ file generated! -> "%s"'%dst_file)


#TEST_01()


####
##  Utils for voxel, matrix, and color manipulation. From PC to mesh (3D reconstruction).
#

def intensity_resampling(pcd, max_value, bins=0):
    '''
        downsamling intensity values of 3D volume
    '''
    if(bins>0 and bins<max_value):
        bins += 1 # 0 is background color 
        border = np.floor(max_value/bins)
        print('Resampling intensity values')
        for i in trange(bins-1):
            pcd[(pcd>=border*i) & (pcd<border*(i+1))] = border*i
        #upper lable case
        pcd[pcd>=border*(bins-1)]=max_value
    return pcd

def GetMesh(file, labels):
    '''
        gets a point cloud (PC) and computes triangulation, returns a mesh reconstruction
        we simplify the intensity levels and use them to lable different objects in the scene
    '''
    # TODO:
    #   - Support for other popular PC file formats such as .PLY
    # DONE:
    #   (1) Convert data to numpy
    #   (2) Reduce resolution of intensity levels
    #   (3) Triangulation loop
    #       - we go over each voxel and its 3 forward neighbors
    #       - if two neighbors have differnt intensities (and none is background), we create a separator
    #       - the voxels are storeda as vertices in 'vertices dictio', the triangles are stored as faces in 'faces dictio'

    ## (1)
    # obtaining data in numpy matrix, plus max intensity value of voxels
    pcd, max_int = PGM3D_GetMetadata(file)
    ## (2)
    # reduce resolution
    pcd = intensity_resampling(pcd,max_int,labels)
    ## (3)
    u_intensites = np.sort(np.unique(pcd))
    background = u_intensites[0]
    # if first voxel is a point (starting point for triangulation), we padd the volume with background to ease 3 neighbor triangulation
    if (pcd[0,0,0]!=background):
        m,n,p = pcd.shape
        M = np.full((m+2,n+2,p+2),background)
        M[1:-1,1:-1,1:-1] = pcd
        pcd = M

    # create data structures to store vertices and faces, will be grouped by intensity
    vertices = {}
    faces = {}
    # initialize so we do not run into problems when saving to file
    for i in range(1,len(u_intensites)):
        vertices[i] = []
        faces[i] = []

    


