import numpy as np 
import matplotlib.pyplot as plt  
import matplotlib
matplotlib.use('WxAgg')
from scipy import interpolate as interp
from pydicom import dcmread
from matplotlib.widgets import Slider
import cv2
ds = dcmread('piramide2.dcm')

import SimpleITK as sitk




class Perfil():
    def __init__(self,mapIntesidad,imagen,figura,ax):
        self.fig=figura
        self.ax=ax
        self.aray=imagen
        self.mapeo=mapIntesidad
        k=fig.ginput(2)
        self.x1=k[0][0]
        self.y1=k[0][1]
        self.x2=k[1][0]
        self.y2=k[1][1]
        self.longes=np.sqrt((self.x2-self.x1)**2+(self.y2-self.y1)**2)
        self.xa=0
        self.ya=0
        self.fig2, self.ax2 = plt.subplots()
        self.line,=self.ax.plot([self.x1,self.x2],[self.y1,self.y2])
        self.pintarPerfil()
        
        self.cidPress=self.fig.canvas.mpl_connect('button_press_event', self.click)
        self.cidSoltar=''
        self.cidMover=''
    def click(self,event):
        self.xa=event.xdata
        self.ya=event.ydata
        self.cidMover=self.fig.canvas.mpl_connect('motion_notify_event', self.mover)
        self.cidSoltar=self.fig.canvas.mpl_connect('button_release_event', self.soltar)
    def mover(self,event):
        despx=event.xdata-self.xa
        despy=event.ydata-self.ya   
        self.xa=event.xdata
        self.ya=event.ydata
        self.x1=self.x1+despx
        self.x2=self.x2+despx
        self.y1=self.y1+despy
        self.y2=self.y2+despy
        self.pintarPerfil()
    def soltar(self,event): 
        self.fig.canvas.mpl_disconnect(self.cidSoltar)
        self.fig.canvas.mpl_disconnect(self.cidMover)
    def pintarPerfil(self):
        m=(self.y2-self.y1)/(self.x2-self.x1)
        b=self.y1-m*self.x1
        x=np.linspace(self.x1,self.x2,300)
        y=m*x+b
        self.line.set_data([x[0],x[-1]],[y[0],y[-1]])
        ys=np.zeros(x.shape[0])
        for i in range(x.shape[0]):
            ys[i]=self.mapeo(x[i],y[i])
        print(ys[0:10])
        xs=np.linspace(0,self.longes,ys.shape[0])
        self.ax2.clear()
        
        self.ax2.plot(xs,ys)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.fig2.canvas.draw()
        self.fig2.canvas.flush_events()

mapaDosisf=np.load("PiramideDosis.npy")

plt.imshow(mapaDosisf)
plt.show()
mapaDosisf=mapaDosisf/6.47
dsize=(512,512)
mapaDosisf=cv2.resize(mapaDosisf, dsize, interpolation = cv2.INTER_NEAREST)
mapaDosis=ds.pixel_array/np.max(ds.pixel_array)        
"""


fig, ax = plt.subplots()
ax.imshow(mapaDosis,cmap=plt.cm.gray)
"""
x=np.linspace(0,mapaDosis.shape[1],mapaDosis.shape[1])
y=np.linspace(0,mapaDosis.shape[0],mapaDosis.shape[0])
f=interp.interp2d(x,y,mapaDosis,fill_value=0)
"""
k=fig.ginput(2)
x1=k[0][0]
y1=k[0][1]
x2=k[1][0]
y2=k[1][1]
m=(y2-y1)/(x2-x1)
b=y1-m*x1
xs=np.linspace(x1,x2,300)
ys=m*xs+b
ax.plot(xs,ys)
print(x1,x2,y1,y2)
print(xs)
print(ys)
z=np.zeros(300)
for i in range(300):
    z[i]=f(xs[i],ys[i])
ls=np.linspace(0,1,300)
plt.figure()
plt.plot(ls,z)
plt.show()
"""
x=np.linspace(-5,5,512)
y=np.linspace(-5,5,512)
#Re=Perfil(f,mapaDosis,fig,ax)
fig, ax = plt.subplots()
axR = plt.axes([0.25, .03, 0.50, 0.02])
spor = Slider(axR, '%', 0, 100.0, valinit=50, valstep=1)
def update(val):
    iv=spor.val
    ax.clear()
    ax.contour(x, y, mapaDosis - iv/100.0, levels = [0],colors=['red'])
    ax.contour(x, y, mapaDosisf - iv/100.0, levels = [0],colors=['blue'])
    fig.canvas.draw_idle()
spor.on_changed(update)    
#plt.contour(x, y, f(x,y) - 0.4, levels = [0],colors=['red'])
plt.show()
