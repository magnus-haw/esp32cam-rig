import pyvista as pv
import numpy as np
from scipy.interpolate import griddata
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

p = pv.Plotter()
mesh = pv.read("~/Desktop/texturedMesh.obj")
tex = pv.read_texture("~/Desktop/texture_1001.png")

#p.add_mesh(mesh, texture=tex)

### Locate center
#center = np.mean(mesh.points, axis=0)
center = np.array([0.07585015, 0.04770663, 1.5445325 ])
trans = mesh.translate(-center, inplace=False)

### Fit axes to top surface
# pca = PCA(n_components=3)
# pca.fit(mesh.points)
# print(pca.components_)
# print(pca.explained_variance_)
#axes = pca.components_

axes = np.matrix([[-0.82504946,  0.5166884,  -0.22875008],
                 [-0.5648014,  -0.76633453,  0.306155  ],
                 [0.01711233,  -0.3817913,  -0.9240901 ]])
rotmtrx = np.zeros((4,4))
rotmtrx[0:3,0:3] = axes.T.I
rotmtrx[3,3]=1

rotate = trans.transform(rotmtrx,inplace=False)
scaled = rotate.scale(6.283*np.ones(3),inplace=False)
XYZ = scaled.points
Z= XYZ[:,2]

#clipped = rotate.clip_box(bounds)
clipped,_ = scaled.remove_points(Z<-.2)
p.add_mesh(scaled, texture=tex)
p.add_mesh(clipped, color="red", show_edges=True)

for ax in axes:
    arrow = pv.Arrow(start=(0,0,0), direction=(0,0,1), scale=1)
    p.add_mesh(arrow, color="red")

_ = p.add_axes(line_width=5, labels_off=True)

XYZ = clipped.points
Z= XYZ[:,2]

n=1000
x = np.linspace(-2.2,2.2, n)
y = np.linspace(-2.2,2.2, n)
xv, yv = np.meshgrid(x, y)
output = griddata(XYZ[:,0:2],Z,(xv,yv))
plt.imshow(output,extent=(-2.2, 2.2, -2.2, 2.2),origin='lower')
plt.colorbar()
plt.show()

p.show()