import open3d as o3d
import numpy as np

# loading point cloud
pcd = o3d.io.read_point_cloud('./data/fragment.ply')
print(pcd)
print(np.asarray(pcd.points))

# visualizing point cloud
o3d.visualization.draw_geometries([pcd])

# automatic surface reconstruction (point cloud -> mesh) using dense point cloud
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, 0.04)
mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)

# lets present a more challenging scenario, using sparse point cloud
# voxel downsampling
pcd_down = pcd.voxel_down_sample(voxel_size=0.05)
o3d.visualization.draw_geometries([pcd_down])

mesh_down = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd_down, 0.1)
mesh_down.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh_down], mesh_show_back_face=True)