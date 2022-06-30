#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkQuadric
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersSources import (
    vtkCylinderSource,
    vtkSphereSource
)
from vtkmodules.vtkIOGeometry import vtkOBJReader
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

import sys

def main():
    colors = vtkNamedColors()

    fileNameModel = sys.argv[1]
    fileNameSecondModel = sys.argv[2]

    renderers = OrderedDict()
    renderers['WireframeSphereRenderer'] = CreateSphere(1)
    renderers['fWireframeModelRenderer'] = CreateModel(1, fileNameModel)
    renderers['WireframeIsoSurfaceRenderer'] = CreateIsoSurface(1)
    renderers['WireframeSecondModelRenderer'] = CreateSecondModel(1, fileNameSecondModel)
    
    renderers['flatSphereRenderer'] = CreateSphere(2)
    renderers['flatModelRenderer'] = CreateModel(2, fileNameModel)
    renderers['flatIsoSurfaceRenderer'] = CreateIsoSurface(2)
    renderers['flatSecondModelRenderer'] = CreateSecondModel(2, fileNameSecondModel)
    
    renderers['GhourandSphereRenderer'] = CreateSphere(3)
    renderers['GhourandModelRenderer'] = CreateModel(3, fileNameModel)
    renderers['GhourandIsoSurfaceRenderer'] = CreateIsoSurface(3)
    renderers['GhourandSecondModelRenderer'] = CreateSecondModel(3, fileNameSecondModel)

    renderers['PhongSphereRenderer'] = CreateSphere(4)
    renderers['PhongModelRenderer'] = CreateModel(4, fileNameModel)
    renderers['PhongIsoSurfaceRenderer'] = CreateIsoSurface(4)
    renderers['PhongSecondModelRenderer'] = CreateSecondModel(4, fileNameSecondModel)
    
    keys = list(renderers.keys())

    renderWindow = vtkRenderWindow()

    rendererSize = 256
    xGridDimensions = 4
    yGridDimensions = 4

    renderWindow.SetSize(rendererSize * xGridDimensions, rendererSize * yGridDimensions)
    renderWindow.SetWindowName('FlatGhourandPhong - Guilherme Nakahata')

    for row in range(0, yGridDimensions):
        for col in range(0, xGridDimensions):
            viewport = [0] * 4
            viewport[0] = col / xGridDimensions
            viewport[1] = (yGridDimensions - (row + 1)) / yGridDimensions
            viewport[2] = (col + 1) / xGridDimensions
            viewport[3] = (yGridDimensions - row) / yGridDimensions
            index = row * xGridDimensions + col
            renderers[keys[index]].SetViewport(viewport)

    for r in range(0, len(renderers)):
        renderers[keys[r]].SetBackground(colors.GetColor3d('SlateGray'))
        renderers[keys[r]].GetActiveCamera().Azimuth(20)
        renderers[keys[r]].GetActiveCamera().Elevation(30)
        renderers[keys[r]].ResetCamera()
        if r > 3:
            renderers[keys[r]].SetActiveCamera(renderers[keys[r - 4]].GetActiveCamera())

        renderWindow.AddRenderer(renderers[keys[r]])

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    renderWindow.Render()
    interactor.Start()


def CreateSphere(flat):

    colors = vtkNamedColors()
    sphere = vtkSphereSource()
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(sphere.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('Gold'))
    if(flat == 1):
        actor.GetProperty().SetRepresentationToWireframe()
    elif (flat == 2):
        actor.GetProperty().SetInterpolationToFlat()
    elif(flat == 3):
        actor.GetProperty().SetInterpolationToGouraud()
    elif(flat == 4):
        actor.GetProperty().SetInterpolationToPhong()
    renderer = vtkRenderer()
    renderer.AddActor(actor)
    
    
    light = vtkLight();
    light.PositionalOn()
    light.SetPosition(4.0, 5.0,1.0)
    light.SetSpecularColor(255,0,0)
    light.SetIntensity(1)
    light.SetFocalPoint(0,0,0)
    renderer.AddLight(light);
    
    return renderer


def CreateCylinder(flat):

    colors = vtkNamedColors()
    cylinder = vtkCylinderSource()
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(cylinder.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('Lavender'))
    if(flat == 1):
        actor.GetProperty().SetRepresentationToWireframe()
    elif (flat == 2):
        actor.GetProperty().SetInterpolationToFlat()
    elif(flat == 3):
        actor.GetProperty().SetInterpolationToGouraud()
    elif(flat == 4):
        actor.GetProperty().SetInterpolationToPhong()
    renderer = vtkRenderer()
    renderer.AddActor(actor)
    return renderer


def CreateIsoSurface(flat):

    quadric = vtkQuadric()
    quadric.SetCoefficients(1, 2, 3, 0, 1, 0, 0, 0, 0, 0)
    sample = vtkSampleFunction()
    sample.SetSampleDimensions(25, 25, 25)
    sample.SetImplicitFunction(quadric)

    contour = vtkContourFilter()
    contour.SetInputConnection(sample.GetOutputPort())
    range = [1.0, 6.0]
    contour.GenerateValues(5, range)

    contourMapper = vtkPolyDataMapper()
    contourMapper.SetInputConnection(contour.GetOutputPort())
    contourMapper.SetScalarRange(0, 7)
    actor = vtkActor()
    actor.SetMapper(contourMapper)
    if(flat == 1):
        actor.GetProperty().SetRepresentationToWireframe()
    elif (flat == 2):
        actor.GetProperty().SetInterpolationToFlat()
    elif(flat == 3):
        actor.GetProperty().SetInterpolationToGouraud()
    elif(flat == 4):
        actor.GetProperty().SetInterpolationToPhong()
        
    actor.GetProperty().SetDiffuseColor(1,0,0)
    actor.GetProperty().SetDiffuse(1)
    actor.GetProperty().SetSpecular(1)
    actor.GetProperty().SetSpecularPower(30.0)
    
    light = vtkLight()
    light.SetPosition(10, 10, 10)
    light.SetColor(1.0, 1.0, 1.0)
    light.SetLightTypeToCameraLight()
    
    renderer = vtkRenderer()
    
    renderer.AddLight(light)
    renderer.AddActor(actor)
    return renderer


def CreateModel(flat, fileName):

    colors = vtkNamedColors()
    reader = vtkOBJReader()
    reader.SetFileName(fileName)
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('DarkViolet'))
    if(flat == 1):
        actor.GetProperty().SetRepresentationToWireframe()
    elif (flat == 2):
        actor.GetProperty().SetInterpolationToFlat()
    elif(flat == 3):
        actor.GetProperty().SetInterpolationToGouraud()
    elif(flat == 4):
        actor.GetProperty().SetInterpolationToPhong()
        
    actor.GetProperty().SetDiffuseColor(1,0,0)
    actor.GetProperty().SetDiffuse(1)
    actor.GetProperty().SetSpecular(1)
    actor.GetProperty().SetSpecularPower(30.0)
    
    light = vtkLight()
    light.SetPosition(10, 10, 10)
    light.SetColor(1.0, 1.0, 1.0)
    light.SetLightTypeToCameraLight()
    
    renderer = vtkRenderer()
    
    renderer.AddLight(light)
    renderer.AddActor(actor)
    return renderer
    
def CreateSecondModel(flat, fileName):
    colors = vtkNamedColors()
    reader = vtkOBJReader()
    reader.SetFileName(fileName)
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('DarkGreen'))
    if(flat == 1):
        actor.GetProperty().SetRepresentationToWireframe()
    elif (flat == 2):
        actor.GetProperty().SetInterpolationToFlat()
    elif(flat == 3):
        actor.GetProperty().SetInterpolationToGouraud()
    elif(flat == 4):
        actor.GetProperty().SetInterpolationToPhong()
    
    renderer = vtkRenderer()
    renderer.AddActor(actor)
    return renderer


if __name__ == '__main__':
    main()
