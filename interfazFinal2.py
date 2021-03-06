#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.6 on Thu Nov 12 23:01:15 2020
#

import numpy as np
import wx
import wx.lib.agw.aui as aui
import wx.lib.mixins.inspection as wit

from dialogoCalibracionAlternativo import DialogoCalibracion
from dialogoSeleccionDosis import *
from claseCalibracion import *
from claseDialogoBackground import *
from panelSeleccionDosis import *
from dialogoMapaDosis import *
from filtradoImagenes import filtrar_imagen
from panelMapaDosis2 import *
from panelMapaDosis1 import *
from dialogoComparacionPlan import *
from panelComparacionAPlan import *
from imagenMatplotlibLibre import *

import matplotlib as mpl
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar

import tifffile as tiff
from skimage.transform import rescale

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

def leerDosis(nombre_archivo):
    """Reads a set of dose values from a txt file"""
    dosis=np.genfromtxt(nombre_archivo)
    return dosis.tolist()

def poner_imagen_en_punto(imgPoner,tamanoGrande,centroImPoner,centroGrande):
    """Returns a recentered image given the center in a bigger frame"""
    resp=np.zeros(tamanoGrande)
    xc=int(centroImPoner[0])
    yc=int(centroImPoner[1])
    corr=0
    if xc%2!=0:
        corr=1
    x=centroGrande[0]
    y=centroGrande[1]
    resp[x-xc:x+(imgPoner.shape[0]-xc),y-yc:y+(imgPoner.shape[1]-yc)]=imgPoner
    return resp
    
class Calibracion():
    def __init__(self,figuras,nombresArchivos,panelDosis):
        self.panelesMatplot=figuras
        self.nombresArchivos=nombresArchivos
        self.panelDosis=panelDosis
        
        self.fondoCero=[]
        self.fondoNegro=[]

class MapaDeDosis():
    def __init__(self,imagenOriginal,mapaCalculado):
        self.imagenOriginal=imagenOriginal
        self.mapaCalculado=mapaCalculado

class ComparacionAPlan():
    def __init__(self,imagenEscan,imagenCalculada):
        self.imScan=imagenEscan
        self.imCalc=imagenCalculada
        
        
class ImagenCuadernoMatplotlib(wx.Panel):
    """Is a panel showing a matplotlib image in the main window of the program"""
    def __init__(self, parent, id=-1, dpi=None, **kwargs):
        wx.Panel.__init__(self, parent, id=id, **kwargs)
        self.figure = mpl.figure.Figure(dpi=dpi)
        self.axA=self.figure.gca()
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.Text = wx.StaticText( self, wx.ID_ANY, u"  Available Channels  ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Text.Wrap( -1 )
        mouseMoveID = self.canvas.mpl_connect('motion_notify_event',self.onMotion)
        self.identificador=0
        self.tipo=''
        self.rutaImagen=''
        self.arrayIma=np.zeros(5)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        sizer.Add(self.Text,0, wx.LEFT | wx.EXPAND)
        #sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()
        
    def onMotion(self, evt):
        """Show cursor position in a label under the frame! Doesn't work well yet"""
        xdata = evt.xdata
        ydata = evt.ydata
        try:
            x = round(xdata,4)
            y = round(ydata,4)
        except:
            x = ""
            y = ""
        if self.arrayIma.shape[0]<6:    
            self.Text.SetLabelText("%s , %s " % (x,y))
        else:
            if x!='' and y!='':
                self.Text.SetLabelText(str(x)+' , '+str(y)+' , '+str(self.arrayIma[int(y),int(x)]))   


class MyFrame(wx.Frame):
    """The main class of the program
    
    Contains all the information about the current session
    The pages are stored in a list named paginas, it is initiallized with a default image
    The current page is stored in paginaActual
    The image being displayed is stored as a numpy array in the arayActual list
    The configuration dictionary stores information about the scanner resolution and color deep, as well as default filtering process
    A fileTree named arbolArchivos is used to keep track of current pages open in the session
    The panels ins the session are stored in calibraciones list if they correspond to a calibration process
    in the mapaDeDosis list if they correspond to dose map analysis
    in the comparacionesAPlan list if they correspond to comparison with a given plan.
    """
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1366, 741))
        self.notebookImagenes = aui.AuiNotebook(self, wx.ID_ANY)
        
        self.paginas=[]
        self.paginas.append(ImagenCuadernoMatplotlib(self.notebookImagenes))
        self.paginaActual=self.paginas[0]
        self.arayActual=[]
        self.araySinIrra=[]
        self.araySinLuz=[]
        
        self.configuracion={"BitCanal":16,"Filtros":['mediana','promedio'],"ppi":100}
        
        
        self.arbolArchivos = wx.TreeCtrl(self, wx.ID_ANY,style=wx.TR_LINES_AT_ROOT)
        self.panelVariable = wx.Panel(self, wx.ID_ANY)
        self.calibraciones=[]
        self.mapasDeDosis=[]
        self.comparacionesAPlan=[]
        self.numeroPags=0
        
        # Menu Bar with all options avaiable
        self.frame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Guardar...", "")
        self.Bind(wx.EVT_MENU, self.guardar, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Abrir...", "")
        self.Bind(wx.EVT_MENU, self.abrir, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Cerrar", "")
        self.Bind(wx.EVT_MENU, self.cerrar, id=item.GetId())
        self.frame_menubar.Append(wxglade_tmp_menu, "Archivo")
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Generar calibracion", "")
        self.Bind(wx.EVT_MENU, self.calibrarNueva, id=item.GetId())
        self.frame_menubar.Append(wxglade_tmp_menu, "Calibracion")
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Generar mapa", "")
        self.Bind(wx.EVT_MENU, self.mapaNuevo, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Realizar comparacion", "")
        self.Bind(wx.EVT_MENU, self.compararMapas, id=item.GetId())
        self.frame_menubar.Append(wxglade_tmp_menu, "Mapas de dosis")
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Promediador", "")
        self.Bind(wx.EVT_MENU, self.promediarImagenes, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Apilar", "")
        self.Bind(wx.EVT_MENU, self.apilarImagenes, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Filtrar", "")
        self.Bind(wx.EVT_MENU, self.filtrarImagenes, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Configuracion", "")
        self.Bind(wx.EVT_MENU, self.cambiarConfiguracion, id=item.GetId())
        self.frame_menubar.Append(wxglade_tmp_menu, "Herramientas")
        self.SetMenuBar(self.frame_menubar)
        # Menu Bar end
        self.FilmQADog_statusbar = self.CreateStatusBar(1, wx.STB_DEFAULT_STYLE)
        
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED,self.cambioPagina,self.notebookImagenes)

        self.__set_properties()
        self.__do_layout()

        # end wxGlade

    def __set_properties(self):
        """Initialize the FileTree and the status bar"""
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("FilmQADog")
        self.FilmQADog_statusbar.SetStatusWidths([-1])
        
        self.raiz=self.arbolArchivos.AddRoot("FilmQADog")
        ident=self.arbolArchivos.AppendItem(self.raiz,"Bienvenido")
        self.arbolArchivos.ExpandAll()

        # statusbar fields
        FilmQADog_statusbar_fields = ["FilmQADog_statusbar"]
        for i in range(len(FilmQADog_statusbar_fields)):
            self.FilmQADog_statusbar.SetStatusText(FilmQADog_statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        """Do the layout of the main program, acommodates panels and set the initial image"""
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.notebookImagenes, 2, wx.EXPAND, 0)
        self.sizer_2.Add(self.arbolArchivos, 1, wx.EXPAND, 0)
        self.sizerPanel=self.sizer_2.Add(self.panelVariable, 1, wx.EXPAND, 0)
        sizer_1.Add(self.sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        
        
        self.notebookImagenes.AddPage(self.paginas[0], "Bienvenido")
        figInicial=self.paginas[0].figure
        a1=figInicial.gca()
        im = tiff.imread('filmQAPerro.tif')
        self.arayActual=im
        a1.imshow(im)
        self.Layout()
        # end wxGlade

    def calibrarNueva(self, event):  # wxGlade: MyFrame.<event_handler>
        """This method initializes a calibration process event.
        
        First it shows a calibration panel, where all information about the calibration files is filled out
        Next, all received images are filtered following the default configuration
        Finally a panelSeleccionDosis is created to select the ROI's that will be used in the image

         """
        dialogoCalibracion=DialogoCalibracion(self)
        dialogoCalibracion.ShowModal()
        if dialogoCalibracion.resultado!='cancelar':
            self.arayActual=tiff.imread(dialogoCalibracion.nombreArchivos[0])
            self.araySinIrra=0*self.arayActual
            self.araySinLuz=0*self.arayActual
            
            if(dialogoCalibracion.background):
                dialogoBackground=DialogoBackground(self)
                dialogoBackground.ShowModal()
                fon=False
                if dialogoBackground.resultado[0]!='cancelar' and dialogoBackground.resultado[0]!='':
                    self.araySinIrra=tiff.imread(dialogoBackground.resultado[0])
                    fon=True
                if(dialogoBackground.resultado[0]!='cancelar' and dialogoBackground.resultado[1]!=''):
                    self.araySinLuz=tiff.imread(dialogoBackground.resultado[1])
                    if fon:
                        self.araySinIrra=self.araySinIrra-self.araySinLuz
                        
            if(dialogoCalibracion.filtrar):
                self.arayActual=filtrar_imagen(self.arayActual,self.configuracion["Filtros"])
                self.araySinIrra=filtrar_imagen(self.araySinIrra,self.configuracion["Filtros"])
            
            calibracionActual=Calibracion([],[],[])
            rez=self.arbolArchivos.AppendItem(self.raiz,"Calibracion "+str(len(self.calibraciones)+1))
            for nombreImagen in dialogoCalibracion.nombreArchivos:    
                self.paginas.append(ImagenCuadernoMatplotlib(self.notebookImagenes))
                self.notebookImagenes.AddPage(self.paginas[-1], "Calibracion "+str(len(self.calibraciones)+1))
                self.numeroPags=self.numeroPags+1
                self.paginas[-1].identificador=self.numeroPags
                self.paginas[-1].tipo='cali'
                self.paginas[-1].rutaImagen=nombreImagen
                nuem=self.notebookImagenes.GetPageCount()-1
                self.notebookImagenes.SetSelection(nuem)
                figActual=self.paginas[-1].figure
                self.paginaActual=self.paginas[-1]
                a1=figActual.gca()
                self.arayActual=tiff.imread(nombreImagen)
                self.paginas[-1].arrayIma=self.arayActual
                #self.arayActual=self.arayActual-self.araySinLuz
                if(dialogoCalibracion.filtrar):
                    self.paginas[-1].arrayIma=filtrar_imagen(self.arayActual,self.configuracion["Filtros"])
                    self.arayActual=self.paginas[-1].arrayIma
                #WARNING! Rescalating may cause lose of precission    
                escalado=(self.arayActual/2**self.configuracion["BitCanal"])*255
                a1.imshow(escalado.astype(int)) 
                calibracionActual.panelesMatplot.append(self.paginas[-1])
                calibracionActual.nombresArchivos.append(nombreImagen)
                self.arbolArchivos.AppendItem(rez,"Imagen "+str(len(calibracionActual.nombresArchivos)))
                
                
            dosisReal=leerDosis(dialogoCalibracion.nombreArchivoDos)
            
            
            self.panelVariable=PanelSeleccionDosis(self,dosis=dosisReal,canal=dialogoCalibracion.tipoCanal,curva=dialogoCalibracion.tipoCurva)
            calibracionActual.panelDosis=self.panelVariable
            calibracionActual.fondoCero=self.araySinIrra
            calibracionActual.fondoNegro=self.araySinLuz
            self.calibraciones.append(calibracionActual)
            self.sizer_2.Remove(1)
            self.sizer_2.Add(self.panelVariable, 1, wx.EXPAND, 0)
            
            
            self.Layout()
        event.Skip()

    def abrir(self, event):  # wxGlade: MyFrame.<event_handler>
        """Opens a file that makes sense to the programs
        
        It can be a .calib file, which contains the information about a calibration
        Or a .dcm file, correponding to a dose map to be analyzed
        """
        dial=wx.FileDialog(self,name="Seleccione archivo",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        nombreAr=''
        if dial.ShowModal()==wx.ID_OK:
            nombreAr=dial.GetPath()
        sufix=nombreAr.split('.')[1]
        if sufix=='calibr':
            datosCalib=leer_Calibracion(nombreAr)
            dosis=datosCalib["Dosis"]
            grafica=ImagenMatplotlibLibre(self,style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
            grafica.ax.grid()
            grafica.ax.set_xlabel("Dosis(Gy)")
            labelss=datosCalib["labels"]
            print(datosCalib["TipoCanal"])
            if datosCalib["TipoCanal"]!="Multicanal":
                grafica.ax.set_ylabel("Densidad ??ptica")
                grafica.ax.text(0, 0.4, labelss[0], color='black', 
                     bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'))
                netODR=datosCalib["Dopticas"][0][0]
                netODG=datosCalib["Dopticas"][0][1]
                netODB=datosCalib["Dopticas"][0][2]
            else:
                grafica.ax.set_ylabel("Transmitancia")
                grafica.ax.text(8.2, 0.65, labelss[0], color='black', 
                     bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1'))
                netODR=datosCalib["Dopticas"][1][0]
                netODG=datosCalib["Dopticas"][1][1]
                netODB=datosCalib["Dopticas"][1][2]
                
            varODR=datosCalib["Incertidumbres"][0]
            varODG=datosCalib["Incertidumbres"][1]
            varODB=datosCalib["Incertidumbres"][2]
            fR=datosCalib["funcionesRGB"][0]
            fG=datosCalib["funcionesRGB"][1]
            fB=datosCalib["funcionesRGB"][2]
            pOptimos=datosCalib["Parametros"]
            grafica.ax.errorbar(dosis,netODR,yerr=varODR,color='r',fmt='o',markersize=2)
            grafica.ax.errorbar(dosis,netODG,yerr=varODG,color='g',fmt='o',markersize=2)
            grafica.ax.errorbar(dosis,netODB,yerr=varODB,color='b',fmt='o',markersize=2)
            xasR=np.linspace(netODR[0],netODR[-1]-0.005,100)
            xasG=np.linspace(netODG[0],netODG[-1]-0.005,100)
            xasB=np.linspace(netODB[0],netODB[-1]-0.005,100)
            print(xasR)
            yasR=fR(xasR)
            yasG=fG(xasG)
            yasB=fB(xasB)

            grafica.ax.plot(yasR,xasR,'r--',label=labelss[1])
            grafica.ax.plot(yasG,xasG,'g--',label=labelss[2])
            grafica.ax.plot(yasB,xasB,'b--',label=labelss[3])
            SR=np.sum(((dosis-fR(netODR)))**2)
            SG=np.sum(((dosis-fG(netODG)))**2)
            SB=np.sum(((dosis-fB(netODB)))**2)

            grafica.figure.legend(loc=7)
            grafica.figure.tight_layout()
            grafica.figure.subplots_adjust(right=0.75)
            
            grafica.Show() 
        event.Skip()

    def cerrar(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'cerrar' not implemented!")
        event.Skip()

    def guardar(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'calibrar' not implemented!")
        event.Skip()

    def mapaNuevo(self, event):  # wxGlade: MyFrame.<event_handler>
        """Creates a new dose map with a previously generated calibration curve .calib and a tiff image
        
        Here is defined which set up will be used for the calibration, including selection of multichannel or single channel route

        """
        dialMapa=DialogoMapaDosis(self)
        dialMapa.ShowModal()
        if dialMapa.resultado=='cancelar':
            return 
        mapaNe=MapaDeDosis([],[])  
         
        datosCalib=leer_Calibracion(dialMapa.rutaCalibracion)
        image=tiff.imread(dialMapa.rutaImagen)
        self.araySinIrra=0*image
        ceR=self.araySinIrra[:,:,0]+datosCalib["Ceros"][0][0]
        ceG=self.araySinIrra[:,:,1]+datosCalib["Ceros"][1][0]
        ceB=self.araySinIrra[:,:,2]+datosCalib["Ceros"][2][0]
        self.araySinIrra=np.dstack((ceR,ceG,ceB))*(2**self.configuracion["BitCanal"])
        self.araySinLuz=0*image

                
        if dialMapa.corrBackground:
            dialogoBackground=DialogoBackground(self)
            dialogoBackground.ShowModal()
            fon=False
            
            if dialogoBackground.resultado[0]!='cancelar' and dialogoBackground.resultado[0]!='':
                
                if datosCalib["TipoCanal"]=="Multicanal":
                    self.araySinIrra=(self.araySinIrra-tiff.imread(dialogoBackground.resultado[0]))
                else:
                    self.araySinIrra=tiff.imread(dialogoBackground.resultado[0])
                fon=True
                
            if(dialogoBackground.resultado[0]!='cancelar' and dialogoBackground.resultado[1]!=''):
                self.araySinLuz=tiff.imread(dialogoBackground.resultado[1])
                image=image-self.araySinLuz
                if fon:
                    self.araySinIrra=self.araySinIrra-self.araySinLuz
        else:
            if datosCalib["TipoCanal"]=="Multicanal":
                self.araySinIrra=0*image
            
            
        if dialMapa.filtrar:
            image=filtrar_imagen(image,self.configuracion["Filtros"])
            if datosCalib["TipoCanal"]!="Multicanal":
                self.araySinIrra=filtrar_imagen(self.araySinIrra,self.configuracion["Filtros"])
            
        self.arayActual=image
        self.paginas.append(ImagenCuadernoMatplotlib(self.notebookImagenes))
        self.notebookImagenes.AddPage(self.paginas[-1], "Mapa de dosis "+str(len(self.mapasDeDosis)+1))
        self.numeroPags=self.numeroPags+1
        self.paginas[-1].identificador=self.numeroPags
        self.paginas[-1].tipo='md1'
        self.paginas[-1].rutaImagen=dialMapa.rutaImagen
        nuem=self.notebookImagenes.GetPageCount()-1
        self.notebookImagenes.SetSelection(nuem)
        figActual=self.paginas[-1].figure
        self.paginaActual=self.paginas[-1]
        a1=figActual.gca()
        self.paginas[-1].arrayIma=self.arayActual
        escalado=(self.arayActual/2**self.configuracion["BitCanal"])*255
        a1.imshow(escalado.astype(int))
        

        
        self.sizer_2.Remove(1)
        self.panelVariable=PanelMapaDosis1(self,dialMapa.rutaCalibracion)
        self.sizer_2.Add(self.panelVariable, 1, wx.EXPAND, 0)
        self.Layout()
        event.Skip()

    def compararMapas(self, event): 
        """Starts a comparison process between two dcm dose maps
        
        Here is defined which set up will be used for the gamma analysis
        
        """
        
        dialComparar=DialogoComparacionPlan(self)
        dialComparar.ShowModal()
        if dialComparar.resultado=='cancelar':
            return
        dicomPlan=pydicom.dcmread(dialComparar.rutaPlan)
        dicomEscan=pydicom.dcmread(dialComparar.rutaEscan)
        arrayPlan=dicomPlan.pixel_array
        arrayEscan=dicomEscan.pixel_array
        dicomPlan.IsocenterPosition=[int(arrayPlan.shape[0]/2),int(arrayPlan.shape[1]/2),0]
        dmm=0
        if dicomPlan.PixelSpacing[0]>=dicomEscan.PixelSpacing[0]:
            reescaldo=np.array(dicomPlan.PixelSpacing)/np.array(dicomEscan.PixelSpacing)
            reescaldo=1.0/reescaldo
            arrayEscan=rescale(dicomEscan.pixel_array,reescaldo,anti_aliasing=False)
            dicomEscan.IsocenterPosition[0]=int(dicomEscan.IsocenterPosition[0]*reescaldo[0])
            dicomEscan.IsocenterPosition[1]=int(dicomEscan.IsocenterPosition[1]*reescaldo[1])
            dmm=dicomPlan.PixelSpacing[0]
        else:
            reescaldo=np.array(dicomEscan.PixelSpacing)/np.array(dicomPlan.PixelSpacing)
            reescaldo=1.0/reescaldo
            arrayPlan=rescale(dicomPlan.pixel_array,reescaldo,anti_aliasing=False)
            dicomPlan.IsocenterPosition[0]=int(dicomPlan.IsocenterPosition[0]*reescaldo[0])
            dicomPlan.IsocenterPosition[1]=int(dicomPlan.IsocenterPosition[1]*reescaldo[1])
            dmm=dicomEscan.PixelSpacing[0]
            
        txi=max(dicomPlan.IsocenterPosition[0],dicomEscan.IsocenterPosition[0])
        txd=max(arrayEscan.shape[0]-dicomEscan.IsocenterPosition[0],arrayPlan.shape[0]-dicomPlan.IsocenterPosition[0])
        tya=max(dicomPlan.IsocenterPosition[1],dicomEscan.IsocenterPosition[1])
        tyb=max(arrayEscan.shape[1]-dicomEscan.IsocenterPosition[1],arrayPlan.shape[1]-dicomPlan.IsocenterPosition[1])
        tmax=txi+txd
        tamy=tya+tyb
            
        if int(tmax)%2!=0:
            tmax+=1
        if int(tamy)%2!=0:
            tamy+=1



        arrayPlanAjus=poner_imagen_en_punto(arrayPlan,(int(tmax),int(tamy)),dicomPlan.IsocenterPosition,(int(txi),int(tya)))
        arrayEscanAjus=poner_imagen_en_punto(arrayEscan,(int(tmax),int(tamy)),(dicomEscan.IsocenterPosition[1],dicomEscan.IsocenterPosition[0]),(int(txi),int(tya)))
        
        
        rez=self.arbolArchivos.AppendItem(self.raiz,"Comparacion a plan  "+str(len(self.comparacionesAPlan)+1))
        self.arayActual=[arrayPlanAjus,arrayEscanAjus]
        self.paginas.append(ImagenCuadernoMatplotlib(self.notebookImagenes))
        self.notebookImagenes.AddPage(self.paginas[-1], "Comparacion a plan "+str(len(self.comparacionesAPlan)+1))
        self.numeroPags=self.numeroPags+1
        self.paginas[-1].identificador=self.numeroPags
        self.paginas[-1].tipo='compa'
        self.paginaActual=self.paginas[-1]
        nuem=self.notebookImagenes.GetPageCount()-1
        self.notebookImagenes.SetSelection(nuem)
        figActual=self.paginas[-1].figure
        self.paginaActual=self.paginas[-1]
        a1=figActual.gca()
        

        arrayPlanAjus=arrayPlanAjus*dicomPlan.DoseGridScaling
        arrayEscanAjus=arrayEscanAjus*dicomEscan.DoseGridScaling
        
        arrayPlanAjus=arrayPlanAjus/np.max(arrayPlanAjus)
        arrayEscanAjus=arrayEscanAjus/np.max(arrayEscanAjus)
        
        self.arayActual=[arrayPlanAjus,arrayEscanAjus]
        self.paginas[-1].arrayIma=[arrayPlanAjus,arrayEscanAjus]
        
        
        self.alpha=0.5
        
        
        a1.imshow((1.0-self.alpha)*self.arayActual[0]+self.alpha*self.arayActual[1],cmap=plt.cm.gray)
        self.axR=self.paginaActual.figure.add_axes([0.25, .03, 0.50, 0.02])
        self.alp = Slider(self.axR, 'Alpha', 0, 1, valinit=0.5, valstep=0.01)
        def update(val):
            iv=self.alp.val
            self.alpha=self.alp.val
            self.paginaActual.axA.clear()
            self.paginaActual.axA.imshow((1.0-iv)*self.arayActual[0]+iv*self.arayActual[1],cmap=plt.cm.gray)
            self.paginaActual.figure.canvas.draw_idle()
        self.alp.on_changed(update) 
        

        self.panelVariable=PanelComparacionAPlan(self,int(dialComparar.tole),int(dialComparar.dist),int(dialComparar.thres),float(dmm))
        self.sizer_2.Remove(1)
        self.sizer_2.Add(self.panelVariable, 1, wx.EXPAND, 0)
        self.Layout()
        event.Skip()

    def promediarImagenes(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'promediarImagenes' not implemented!")
        event.Skip()

    def apilarImagenes(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'apilarImagenes' not implemented!")
        event.Skip()

    def filtrarImagenes(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'filtrarImagenes' not implemented!")
        event.Skip()

    def cambiarConfiguracion(self, event):  # wxGlade: MyFrame.<event_handler>
        print("Event handler 'cambiarConfiguracion' not implemented!")
        event.Skip()
    def cambioPagina(self,event):
        print('cambioPagina')
        pestana=self.notebookImagenes.GetCurrentPage()
        if pestana.tipo=='cali':
            for cals in self.calibraciones:
                for fisa in cals.panelesMatplot:
                    if fisa.identificador==pestana.identificador:
                        self.arayActual=fisa.arrayIma
                        self.araySinIrra=cals.fondoCero
                        self.araySinLuz=cals.fondoNegro
                        self.paginaActual=fisa
                        self.panelVariable=cals.panelDosis
                        print(self.panelVariable.R)
                        break
        
                      
        self.sizer_2.Remove(1)
        self.sizer_2.Add(self.panelVariable, 1, wx.EXPAND, 0)
        self.Layout()
                        
        event.Skip()

# end of class MyFrame

class MyApp(wx.App):
    def OnInit(self):
        self.FilmQADog = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.FilmQADog)
        self.FilmQADog.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
