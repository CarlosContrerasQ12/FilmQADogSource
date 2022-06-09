from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from pydicom import dcmread
from pydicom.data import get_testdata_file
from scipy import interpolate

fpath = get_testdata_file('CT_small.dcm')
ds = dcmread('piramide.dcm')

x=np.linspace(-5,5,512)
y=np.linspace(-5,5,512)

z=ds.pixel_array/np.max(ds.pixel_array)
print(z)
f = interpolate.interp2d(x, y, z, kind='cubic')
X, Y = np.meshgrid(x, y)
fig = plt.figure()
ax = fig.gca(projection='3d')

ax.set_zlim(zmin = 0)
ax.plot_surface(X, Y, z,cmap='viridis', edgecolor='none')
ax.contour(x, y, f(x,y) - 0.4, levels = [0])
ax.contour(x, y, z - 0.4, levels = [0])
plt.show()

# Normal mode:
#print()
#print(f"File path........: {fpath}")
#print(f"SOP Class........: {ds.SOPClassUID} ({ds.SOPClassUID.name})")
#print()

#pat_name = ds.PatientName
#display_name = pat_name.family_name + ", " + pat_name.given_name
#print(f"Patient's Name...: {display_name}")
#print(f"Patient ID.......: {ds.PatientID}")
#print(f"Modality.........: {ds.Modality}")
#print(f"Study Date.......: {ds.StudyDate}")
#print(f"Image size.......: {ds.Rows} x {ds.Columns}")
#print(f"Pixel Spacing....: {ds.PixelSpacing}")

# use .get() if not sure the item exists, and want a default value if missing
#print(f"Slice location...: {ds.get('SliceLocation', '(missing)')}")

# plot the image using matplotlib
print(ds.pixel_array)
plt.imshow(ds.pixel_array, cmap=plt.cm.gray)
plt.figure()
plt.contour(x, y, f(x,y) - 0.4, levels = [0],colors=['red'])
plt.contour(x, y, f(x,y) - 0.1, levels = [0],colors=['green'])
plt.contour(x, y, f(x,y) - 0.8, levels = [0],colors=['blue'])
plt.contour(x, y, f(x,y) - 0.9, levels = [0],colors=['yellow'])
plt.contour(x, y, z - 0.9, levels = [0],colors=['black'])
plt.show()
