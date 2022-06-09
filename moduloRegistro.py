import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from pydicom import dcmread
from skimage.transform import rescale
from matplotlib.widgets import Slider

dicomEscan = dcmread('MapaCorre.dcm')
dicomPlan = dcmread('piramide2.dcm')

def poner_imagen_en_punto(imgPoner,tamanoGrande,puntoEnGrande,puntoEnPoner):
    resp=np.zeros(tamanoGrande)
    x=imgPoner.shape[0]
    y=imgPoner.shape[1]
    if x%2==0:
        cor=0
    else:
        cor=1
    if y%2==0:
        cory=0
    else:
        cory=1 
    resp[puntoEnGrande[0]-int(x/2)+0:puntoEnGrande[0]+int(x/2)+cor+0,puntoEnGrande[1]-int(y/2)+0:puntoEnGrande[1]+int(x/2)+cory+0]=imgPoner
    return resp


reescaldo=np.array(dicomPlan.PixelSpacing)/np.array(dicomEscan.PixelSpacing)
arrayPlan=rescale(dicomPlan.pixel_array,reescaldo,anti_aliasing=False)
centroEscan=int(dicomEscan.pixel_array.shape[0]/2),int(dicomEscan.pixel_array.shape[1]/2)
arrayPlanAjus=poner_imagen_en_punto(arrayPlan,dicomEscan.pixel_array.shape,centroEscan,(0,0))

arrayPlan=arrayPlanAjus/np.max(arrayPlanAjus)

#arrayPlan=dicomPlan.pixel_array/np.max(dicomPlan.pixel_array)
arrayEscan=dicomEscan.pixel_array*dicomEscan.DoseGridScaling/7.06

fixed_image =  sitk.GetImageFromArray(arrayPlan)
moving_image = sitk.GetImageFromArray(arrayEscan)


alpha=0.5
fig=plt.figure()
plt.imshow((1.0-alpha)*arrayPlan+alpha*arrayEscan,cmap=plt.cm.gray)
ax=plt.gca()

axR=fig.add_axes([0.25, .03, 0.50, 0.02])
alp = Slider(axR, 'Alpha', 0, 1, valinit=0.5, valstep=0.01)

def update(val):
    iv=alp.val
    ax.clear()
    ax.imshow((1.0-iv)*arrayPlan+iv*arrayEscan,cmap=plt.cm.gray)
    fig.canvas.draw_idle()
alp.on_changed(update)


initial_transform = sitk.CenteredTransformInitializer(fixed_image, 
                                                      moving_image, 
                                                      sitk.Euler2DTransform(), 
                                                      sitk.CenteredTransformInitializerFilter.GEOMETRY)

moving_resampled = sitk.Resample(moving_image, fixed_image, initial_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())


registration_method = sitk.ImageRegistrationMethod()

# Similarity metric settings.
registration_method.SetMetricAsMeanSquares()
registration_method.SetMetricSamplingStrategy(registration_method.RANDOM)
registration_method.SetMetricSamplingPercentage(0.01)

registration_method.SetInterpolator(sitk.sitkLinear)

# Optimizer settings.
registration_method.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=40, convergenceMinimumValue=1e-6, convergenceWindowSize=10)
registration_method.SetOptimizerScalesFromPhysicalShift()

# Setup for the multi-resolution framework.            
registration_method.SetShrinkFactorsPerLevel(shrinkFactors = [4,2,1])
registration_method.SetSmoothingSigmasPerLevel(smoothingSigmas=[2,1,0])
registration_method.SmoothingSigmasAreSpecifiedInPhysicalUnitsOn()

# Don't optimize in-place, we would possibly like to run this cell multiple times.
registration_method.SetInitialTransform(initial_transform, inPlace=False)

# Connect all of the observers so that we can perform plotting during registration.
#registration_method.AddCommand(sitk.sitkStartEvent, start_plot)
#registration_method.AddCommand(sitk.sitkEndEvent, end_plot)
#registration_method.AddCommand(sitk.sitkMultiResolutionIterationEvent, update_multires_iterations) 
#registration_method.AddCommand(sitk.sitkIterationEvent, lambda: plot_values(registration_method))

final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat64), 
                                               sitk.Cast(moving_image, sitk.sitkFloat64))
                                               
print('Final metric value: {0}'.format(registration_method.GetMetricValue()))
print('Optimizer\'s stopping condition, {0}'.format(registration_method.GetOptimizerStopConditionDescription()))    

moving_resampled = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())


arrayEscan2=sitk.GetArrayViewFromImage(moving_resampled)
arrayPlan2=arrayPlan


alpha2=0.5
fig2=plt.figure()
plt.imshow((1.0-alpha2)*arrayPlan2+alpha2*arrayEscan2,cmap=plt.cm.gray)
ax2=plt.gca()

axR2=fig2.add_axes([0.25, .03, 0.50, 0.02])
alp2 = Slider(axR2, 'Alpha', 0, 1, valinit=0.5, valstep=0.01)

def update(val):
    iv2=alp2.val
    ax2.clear()
    ax2.imshow((1.0-iv2)*arrayPlan2+iv2*arrayEscan2,cmap=plt.cm.gray)
    fig2.canvas.draw_idle()
alp2.on_changed(update)    
                   
plt.show()
