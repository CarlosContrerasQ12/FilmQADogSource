#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.6 on Mon Sep 14 16:06:35 2020
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class DialogoBackground(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.window_1 = wx.FilePickerCtrl(self,message="Seleccione archivo",style=wx.FLP_USE_TEXTCTRL)
        self.window_2 = wx.FilePickerCtrl(self,message="Seleccione archivo",style=wx.FLP_USE_TEXTCTRL)
        self.Aceptar = wx.Button(self, wx.ID_ANY, "Aceptar")
        self.Cancelar = wx.Button(self, wx.ID_ANY, "Cancelar")
        
        

        self.__set_properties()
        self.__do_layout()
        self.resultado=['cancelar']
        
        self.Bind(wx.EVT_BUTTON, self.aceptar, self.Aceptar)
        self.Bind(wx.EVT_BUTTON, self.cancelar, self.Cancelar)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle("Imagenes de Background")
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        grid_sizer_1 = wx.GridSizer(3, 2, 0, 0)
        labelRutaSinIrradiar = wx.StaticText(self, wx.ID_ANY, "Ruta imagen sin irradiar")
        grid_sizer_1.Add(labelRutaSinIrradiar, 2, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.window_1, 1, wx.EXPAND, 0)
        labelRutaSinLuz = wx.StaticText(self, wx.ID_ANY, "Ruta imagen sin luz")
        grid_sizer_1.Add(labelRutaSinLuz, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.window_2, 1, wx.EXPAND, 0)
        grid_sizer_1.Add(self.Aceptar, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.Cancelar, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(grid_sizer_1)
        grid_sizer_1.Fit(self)
        self.Layout()
        
    def aceptar(self, event):  # wxGlade: MyDialog.<event_handler>
        self.resultado=[]
        self.resultado.append(self.window_1.GetPath())
        self.resultado.append(self.window_2.GetPath())
        print(self.resultado)
        self.Close()

    def cancelar(self, event):  # wxGlade: MyDialog.<event_handler>
        self.Close()
        

        # end wxGlade

# end of class MyDialog

class MyApp(wx.App):
    def OnInit(self):
        self.dialog = DialogoBackground(None, wx.ID_ANY, "")
        self.SetTopWindow(self.dialog)
        self.dialog.ShowModal()
        self.dialog.Destroy()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
