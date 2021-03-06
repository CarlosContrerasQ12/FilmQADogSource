#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.6 on Mon Nov  9 23:14:10 2020
#

import wx
import wx.grid
import numpy as np
from claseCalibracion import *
import matplotlib.pyplot as plt

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class DialogoSeleccionDosis(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        print(kwds)
        self.dosis=kwds["dosis"]
        self.tipoCanal=kwds["canal"]
        self.tipoCurva=kwds["curva"]
        self.corrLateral=kwds["lateral"]
        del kwds["dosis"]
        del kwds["canal"]
        del kwds["curva"]
        del kwds["lateral"]
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER 
        wx.Dialog.__init__(self, *args, **kwds)
        self.button_3 = wx.Button(self, wx.ID_ANY, "Nueva ROI")
        self.button_4 = wx.Button(self, wx.ID_ANY, "Nueva Dosis")
        self.button_5 = wx.Button(self, wx.ID_ANY, "Nueva medida")
        self.button_6 = wx.Button(self, wx.ID_ANY, "Calibrar")
        self.grid_1 = wx.grid.Grid(self, wx.ID_ANY, size=(1, 1))
        self.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.onSelectCell, self.grid_1)
        self.parent=args[0]
        self.filaActual=0
        self.colActual=0
        self.R=[[None]*len(self.dosis)]
        self.G=[[None]*len(self.dosis)]
        self.B=[[None]*len(self.dosis)]
        
        self.Rtotal=[]
        self.Gtotal=[]
        self.Btotal=[]
        
        


        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.nuevaRoi, self.button_3)
        self.Bind(wx.EVT_BUTTON, self.NuevaDosis, self.button_4)
        self.Bind(wx.EVT_BUTTON, self.NuevaMedida, self.button_5)
        self.Bind(wx.EVT_BUTTON, self.GenerarCalibracion, self.button_6)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle("Seleccion de ROIs")
        n=len(self.dosis)
        self.grid_1.CreateGrid(n, 2)
        self.grid_1.SetColLabelValue(0, "Dosis")
        self.grid_1.SetColLabelValue(1, "Medida 1")
        for i in range(n):
            self.grid_1.SetCellValue(i,0,str(self.dosis[i]))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_3.Add(self.button_3, 1, wx.EXPAND, 0)
        sizer_3.Add(self.button_4, 1, wx.EXPAND, 0)
        sizer_3.Add(self.button_5, 1, wx.EXPAND, 0)
        sizer_3.Add(self.button_6, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_2.Add(self.grid_1, 2, wx.EXPAND, 0)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        self.Layout()
        # end wxGlade
        
    def onSelectCell(self,event):
        self.filaActual=event.GetRow()
        self.colActual=event.GetCol()
        event.Skip()
        

    def nuevaRoi(self, event):  # wxGlade: MyDialog.<event_handler>
        k=self.parent.paginaActual.ginput(2)
        x1=k[0][0]
        y1=k[0][1]
        x2=k[1][0]
        y2=k[1][1]
        prom=np.mean(self.parent.arayActual[min(int(y1),int(y2)):max(int(y1),int(y2)),min(int(x1),int(x2)):max(int(x1),int(x2)),:],axis=(0,1))
        print(k)
        print(prom)
        print(self.R)
        print(self.filaActual)
        print(self.colActual)
        self.R[self.colActual-1][self.filaActual]=1-prom[0]/2**8
        self.G[self.colActual-1][self.filaActual]=1-prom[1]/2**8
        self.B[self.colActual-1][self.filaActual]=1-prom[2]/2**8
        self.grid_1.SetCellValue(self.filaActual,self.colActual,str(prom[0]/2**8)+';'+str(prom[1]/2**8)+';'+str(prom[2]/2**8))
        event.Skip()

    def NuevaDosis(self, event):  # wxGlade: MyDialog.<event_handler>
        self.grid_1.AppendRows()
        self.dosis.append(0)
        for i in range(len(self.R)):
            self.R[i].append(0)
            self.G[i].append(0)
            self.B[i].append(0)
        self.grid_1.SetCellValue(self.grid_1.GetNumberRows()-1,0,'0')
        event.Skip()

    def NuevaMedida(self, event):  # wxGlade: MyDialog.<event_handler>
        self.grid_1.AppendCols()
        nom=self.grid_1.GetNumberCols()
        self.grid_1.SetColLabelValue(nom-1, "Medida "+str(nom-1))
        self.R.append([None]*len(self.dosis))
        self.G.append([None]*len(self.dosis))
        self.B.append([None]*len(self.dosis))
        event.Skip()

    def GenerarCalibracion(self, event):  # wxGlade: MyDialog.<event_handler>
        self.Rtotal=np.mean(self.R,axis=0)
        self.Gtotal=np.mean(self.G,axis=0)
        self.Btotal=np.mean(self.B,axis=0)
        for i in range(self.grid_1.GetNumberRows()):
            self.dosis[i]=float(self.grid_1.GetCellValue(i,0))
        np.savetxt('dosishp.txt',self.dosis)
        np.savetxt('Rhp.txt',self.Rtotal)
        np.savetxt('Ghp.txt',self.Gtotal)
        np.savetxt('Bhp.txt',self.Btotal)
        
        #Rar=np.array(self.Rtotal)
        #Rar=Rar-Rar[0]
        #plt.scatter(self.dosis,Rar)
        #plt.show()
        fdlg = wx.FileDialog(self, "Guardar calibracion",wildcard="calibraciones (*.txt)|*.txt", style=wx.FD_SAVE)
        fdlg.SetFilename("calibracion-")
        nombreArchivo=''
        if fdlg.ShowModal() == wx.ID_OK:
                nombreArchivo = fdlg.GetPath() + ".txt"
        calibr=CalibracionImagen(self.Rtotal,self.Gtotal,self.Btotal,self.dosis,self.tipoCanal,self.tipoCurva,self.corrLateral)
        calibr.generar_calibracion(nombreArchivo)
        self.Close()
        event.Skip()
        

# end of class MyDialog

class MyApp(wx.App):
    def OnInit(self):
        self.dialog = DialogoSeleccionDosis(None,[10,20], wx.ID_ANY, "")
        self.SetTopWindow(self.dialog)
        self.dialog.ShowModal()
        self.dialog.Destroy()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
