#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.6 on Sun Sep 13 14:22:39 2020
#

import wx

# begin wxGlade: dependencies
# end wxGlade




class DialogoCalibracion(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((900, 438))
        #self.SelectorImagen = wx.FilePickerCtrl(self,message="Seleccione archivo",style=wx.FLP_USE_TEXTCTRL|wx.FC_MULTIPLE)
        self.SelectorImagen = wx.Button(self, wx.ID_ANY, "Navegar")
        self.CajaTexto=wx.TextCtrl(self,value="",style=wx.TE_READONLY)
        #self.window_1 = wx.FilePickerCtrl(self,message="Seleccione archivo",style=wx.FLP_USE_TEXTCTRL)
        self.SelectorDosis = wx.Button(self, wx.ID_ANY, "Navegar")
        self.CajaTextoDosis=wx.TextCtrl(self,value="",style=wx.TE_READONLY)
        self.combo_box_canal = wx.ComboBox(self, wx.ID_ANY, choices=["Multicanal", "Canal solo"], style=wx.CB_DROPDOWN)
        self.combo_box_curva = wx.ComboBox(self, wx.ID_ANY, choices=["Racional lineal", "Cubica", "Exponencial polinomica", "Lineal"], style=wx.CB_DROPDOWN)
        self.checkboxFiltrar = wx.CheckBox(self, wx.ID_ANY, "Filtrar")
        self.checkboxBackground = wx.CheckBox(self, wx.ID_ANY, "Background")
        self.Aceptar = wx.Button(self, wx.ID_ANY, "Aceptar")
        self.button_1 = wx.Button(self, wx.ID_ANY, "Cancelar")
        self.nombreArchivos=[]
        self.nombreArchivoDos=''
        
        self.resultado='cancelar'
        self.filtrar=False
        self.background=False
        self.tipoCanal=''
        self.tipoCurva=''
        

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.aceptar, self.Aceptar)
        self.Bind(wx.EVT_BUTTON, self.cancelar, self.button_1)
        self.Bind(wx.EVT_BUTTON, self.buscarIm, self.SelectorImagen)
        self.Bind(wx.EVT_BUTTON, self.buscarDos, self.SelectorDosis)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.SetTitle(u"Calibración Manual")
        self.SetSize((900, 438))
        self.SelectorImagen.SetMinSize((400, 50))
        self.SelectorDosis.SetMinSize((400, 50))
        self.combo_box_canal.SetSelection(0)
        self.combo_box_curva.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        grid_sizer_1 = wx.GridSizer(6, 2, 2, 2)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        labelRutaImagen = wx.StaticText(self, wx.ID_ANY, "Ruta Imagen", style=wx.ALIGN_CENTER)
        grid_sizer_1.Add(labelRutaImagen, 0, wx.ALIGN_CENTER | wx.ALL | wx.FIXED_MINSIZE, 2)
        sizerNav=wx.BoxSizer(wx.HORIZONTAL)
        sizerNav.Add(self.CajaTexto,  1, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.FIXED_MINSIZE, 10)
        sizerNav.Add(self.SelectorImagen, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.FIXED_MINSIZE, 20)
        grid_sizer_1.Add(sizerNav,1, wx.EXPAND, 0)
       
        #grid_sizer_1.Add(self.SelectorImagen, 1, wx.ALIGN_CENTER, 0)
        labelRutaDatosCalibracion = wx.StaticText(self, wx.ID_ANY, "Ruta datos de calibracion")
        grid_sizer_1.Add(labelRutaDatosCalibracion, 0, wx.ALIGN_CENTER | wx.ALL, 0)
        
        #grid_sizer_1.Add(self.window_1, 0, wx.ALIGN_CENTER, 0)
        sizerNav2=wx.BoxSizer(wx.HORIZONTAL)
        sizerNav2.Add(self.CajaTextoDosis,  1, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.FIXED_MINSIZE, 10)
        sizerNav2.Add(self.SelectorDosis, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.FIXED_MINSIZE, 20)
        grid_sizer_1.Add(sizerNav2,1, wx.EXPAND, 0)
        labelTipo = wx.StaticText(self, wx.ID_ANY, "Canal de calibracion")
        grid_sizer_1.Add(labelTipo, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.combo_box_canal, 0, wx.ALIGN_CENTER | wx.FIXED_MINSIZE, 0)
        labelTipoCurva = wx.StaticText(self, wx.ID_ANY, "Tipo de calibracion", style=wx.ALIGN_CENTER)
        grid_sizer_1.Add(labelTipoCurva, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.combo_box_curva, 0, wx.ALIGN_CENTER | wx.FIXED_MINSIZE, 0)
        labelCorecciones = wx.StaticText(self, wx.ID_ANY, "Correcciones")
        grid_sizer_1.Add(labelCorecciones, 0, wx.ALIGN_CENTER, 0)
        sizer_1.Add(self.checkboxFiltrar, 0, 0, 0)
        sizer_1.Add(self.checkboxBackground, 0, wx.EXPAND, 0)
        grid_sizer_1.Add(sizer_1, 0, wx.ALIGN_CENTER | wx.ALL | wx.FIXED_MINSIZE | wx.SHAPED, 0)
        grid_sizer_1.Add(self.Aceptar, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 1)
        grid_sizer_1.Add(self.button_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.SetSizer(grid_sizer_1)
        self.Layout()
        # end wxGlade

    def aceptar(self, event):  # wxGlade: MyDialog.<event_handler>
        self.resultado='aceptar'
        self.tipoCanal=self.combo_box_canal.GetStringSelection()
        self.tipoCurva=self.combo_box_curva.GetStringSelection()
        self.filtrar=self.checkboxFiltrar.GetValue()
        self.background=self.checkboxBackground.GetValue()
        self.Close()
        event.Skip()
        
        
    def buscarIm(self,event):
        dial=wx.FileDialog(self,name="Seleccione archivo",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        if dial.ShowModal()==wx.ID_OK:
            self.nombreArchivos=dial.GetPaths()
            resp=';'.join(self.nombreArchivos)
            self.CajaTexto.SetValue(resp)
            print(self.nombreArchivos)
    def buscarDos(self,event):
        dial=wx.FileDialog(self,name="Seleccione archivo",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if dial.ShowModal()==wx.ID_OK:
            self.nombreArchivoDos=dial.GetPath()
            self.CajaTextoDosis.SetValue(self.nombreArchivoDos)

            
        
        

    def cancelar(self, event):  # wxGlade: MyDialog.<event_handler>
        self.Close()

# end of class MyDialog

class MyApp(wx.App):
    def OnInit(self):
        self.dialog = DialogoCalibracion(None, wx.ID_ANY, "")
        self.SetTopWindow(self.dialog)
        self.dialog.ShowModal()
        self.dialog.Destroy()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()